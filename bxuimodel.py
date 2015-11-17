# -*- coding: utf-8 -*-
__author__ = 'banxi'
import sys
import re
from collections import namedtuple
from jinja2 import Template

char_type_map = {
    'l': 'UILabel',
    'b': 'UIButton',
    'v': 'UIView',
    'i': 'UIImageView',
    'f': 'UITextField',
    't': 'UITextView',
    'pc': 'UIPageControl',
    'dp': 'UIDatePicker',
    'st': 'UIStepper',
    'sw': 'UISwitch',
    'sl': 'UISlide',
    'sc': 'UISegmentedControl',
}
model_type_map = {
    'v': 'UIView',
    't': 'UITableViewCell',
    'c': 'UICollectionViewCell',
}

field_pin_map = {
    'x': 'pinCenterX',
    'y': 'pinCenterY',
    'l': 'pinLeading',
    't': 'pinTop',
    'r': 'pinTrailing',
    'b': 'pinBottom',
    'w': 'pinWidth',
    'h': 'pinHeight',
    'a': 'pinAspectRatio'

}

field_attr_map = {
    'f': 'UIFont.systemFontOfSize',
    'fb': 'UIFont.boldSystemFontOfSize',
    'cdg': 'UIColor.darkGrayColor',
    'cg': 'UIColor.grayColor',
    'clg': 'UIColor.lightGrayColor',
    'cb': 'UIColor.blackColor',
    'cw': 'UIColor.whiteColor',
    'cwa': '+UIColor(white: 1.0, alpha: 1.0)',
    'ch': '+UIColor(hex:0xabc)'
}


class ModelDecl(object):
    def __init__(self, name, superclass):
        self.name = name
        self.superclass = superclass

    @property
    def init_stmts(self):
        return Template('''
    {% if 'TableViewCell' in superclass %}
     override init(style: UITableViewCellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        commonInit()
    }
    {% else %}
      override init(frame: CGRect) {
        super.init(frame: frame)
        commonInit()
     }
     {% endif %}

    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
    }

    override func awakeFromNib() {
        super.awakeFromNib()
        commonInit()
    }
''').render(superclass=self.superclass)


def _field_name_to_type_name(field_name):
    words = re.split('_', field_name)
    return ''.join([word.capitalize() for word in words if word])


def create_construct_exp(type_class):
    if type_class == 'UIButton':
        return 'UIButton(type:.System)'
    else:
        return '{type_class}(frame:CGRectZero)'.format(type_class=type_class)


class UIField(object):
    def __init__(self, name, ftype, constraints, attrs):
        type_class = char_type_map.get(ftype, 'UILabel')
        pure_type_name = type_class.replace('UI', '')
        self.ftype = ftype
        self.field_name = "{name}{type_name}".format(name=name, type_name=pure_type_name)
        self.name = name
        self.type_class = type_class
        self.constraints = constraints
        self.attrs = attrs

    @property
    def declare_stmt(self):
        construct_exp = create_construct_exp(self.type_class)
        return ' let {field_name} = {construct_exp}'.format(field_name=self.field_name, construct_exp=construct_exp)

    @property
    def constraints_stmt(self):
        if not self.constraints:
            return ''
        c_stmts = []
        for c in self.constraints:
            item = parse_field_config_item(c)
            func_name = field_pin_map.get(item.ctype)
            if func_name:
                stmt = '{field_name}.{func_name}({value})'.format(field_name=self.field_name,
                                                                  func_name=func_name,
                                                                  value=item.ctype)
                c_stmts.append(stmt)
        return '\n'.join(c_stmts)

    @property
    def attrs_stmt(self):
        if not self.attrs:
            return ''
        stmts = []
        for attr in self.attrs:
            item = parse_field_config_item(attr)
            func_name = field_attr_map.get(item.ctype)
            if not func_name:
                continue
            no_param = func_name.startswith('+')
            if no_param:
                func_name = func_name.replace('+', '')
            prop_name = 'font' if item.ctype.startswith('f') else 'textColor'
            if self.ftype == 'v':
                # UIView
                prop_name = 'backgroundColor'
            ctx = dict(field_name=self.field_name, prop_name=prop_name, func_name=func_name)
            if no_param:
                if self.ftype == 'b':
                    # UIButton
                    stmt = '{field_name}.setTitleColor({func_name}, forState: .Normal)' .format(**ctx)
                else:
                    stmt = '{field_name}.{prop_name} = {func_name}'.format(**ctx)
            else:
                ctx['value'] = item.value
                if self.ftype == 'b':
                    # UIButton
                    stmt = '{field_name}.setTitleColor({func_name}(value), forState: .Normal)' .format(**ctx)
                else:
                    stmt = '{field_name}.{prop_name} = {func_name}(value)'.format(**ctx)
            stmts.append(stmt)

        return '\n'.join(stmts)


field_pattern = re.compile(r'(?P<fname>\w+)(?:\[(?P<constraints>[\w,]+)\])?(?:\((?P<attrs>[\w,]+)\))?')
int_value_pattern = re.compile(r'(?P<value>\d+)')


def parse_field_info(field_info):
    parts = re.split(':', field_info.strip())
    field_config = parts[0]
    field_config = field_config.replace('"', '')
    matcher = field_pattern.match(field_config)
    groupdict = matcher.groupdict()
    fname = groupdict.get('fname').replace('-', '_')
    constraints_config = groupdict.get('constraints')
    constraints = constraints_config.split(',') if constraints_config else []
    attrs_config = groupdict.get('attrs')
    attrs = attrs_config.split(',') if attrs_config else []

    ftype = None
    if len(parts) > 1:
        ftype = parts[1]
    if not ftype:
        ftype = 'l'

    return UIField(fname, ftype, constraints, attrs)


ConfigItem = namedtuple('ConfigItem', ['ctype', 'value'])


def parse_field_config_item(config):
    c = config.strip()
    m = int_value_pattern.search(c)
    value = ''
    ctype = c
    if m:
        value = m.groupdict().get('value')
    if value:
        ctype = c.replace(value, '')
    return ConfigItem(ctype, value)


def parse_model_name(model_info):
    parts = re.split(':', model_info.strip())
    raw_mname = parts[0][1:]  # drop leading '-'
    raw_mname = raw_mname.replace('-', '_')
    model_name = _field_name_to_type_name(raw_mname)
    mtype = parts[1] if len(parts) > 1 else 'v'
    superclass = model_type_map.get(mtype, 'UIView')
    return ModelDecl(model_name, superclass)


def parse_line(line):
    field_infos = re.split(r';', line)
    model_decl = None
    uifields = []
    for field_info in field_infos:
        field_info = field_info.strip()
        if not field_info:
            continue
        if field_info.startswith('-'):
            model_decl = parse_model_name(field_info)
            continue
        uifield = parse_field_info(field_info)
        if uifield:
            uifields.append(uifield)

    return uifields, model_decl


uimode_tpl = '''
{% for comment in comments %}
  {{ comment }}
{% endfor %}
class {{ model.name }} : {{model.superclass}} {
{% for field in uifields %}
    {{ field.declare_stmt }}
{% endfor %}
    {{ model.init_stmts }}
    func commonInit(){
        let childViews = [{{ childViews }}]
        for childView in childViews{
            {% if 'cell' in model.superclass %}
            contentView.addSubview(childView)
            {% else %}
            addSubview(childView)
            {% endif %}
            childView.translatesAutoresizingMaskIntoConstraints = false
        }
        installConstaints()
        setupAttrs()
    }

    func installConstaints(){
    {% for field in uifields %}
    {{ field.constraints_stmt }}
    {% endfor %}
    }

    func setupAttrs(){
    {% for field in uifields %}
    {{ field.attrs_stmt }}
    {% endfor %}
    }

}
'''


def main():
    uifield_list = []

    comments = []
    last_model_decl = None
    for line in sys.stdin:
        line = line.strip()
        if line:
            comments.append("// " + line)
            uifields, model_decl = parse_line(line)
            if model_decl:
                last_model_decl = model_decl
            if uifields:
                uifield_list.extend(uifields)
    template = Template(uimode_tpl, trim_blocks=True, lstrip_blocks=True)
    childViews = ','.join([f.field_name for f in uifield_list])
    text = template.render(model=last_model_decl, uifields=uifield_list, childViews=childViews, comments=comments)
    print(text)


if __name__ == '__main__':
    main()
