# -*- coding: utf-8 -*-
__author__ = 'banxi'
import sys
import re
from jinja2 import Template
from collections import namedtuple
import itertools

FIELD_DELIMETER = ';'

char_type_map = {
    'l': 'UILabel',
    'b': 'UIButton',
    'v': 'UIView',
    'i': 'UIImageView',
    'f': 'UITextField',
    't': 'UITableView',
    'c': 'UICollectionView',
    'pc': 'UIPageControl',
    'dp': 'UIDatePicker',
    'st': 'UIStepper',
    'sw': 'UISwitch',
    'sl': 'UISlide',
    'sc': 'UISegmentedControl',
    'tc': 'UITableViewCell',
}

type_value_field_map = {
    'l': 'text',
    'f': 'text',
    'sw': 'on',
}

type_value_type_map = {
    'l': 'String',
    'f': 'String',
    'sw': 'Bool'
}

# label:l,label2,button:b,view:v,imageView:i,field:f,addr:tc
def _field_name_to_type_name(field_name):
    words = re.split('_', field_name)
    return ''.join([word.capitalize() for word in words if word])


class UIField(object):
    def __init__(self, name, ftype, constraints, attrs):
        type_class = char_type_map.get(ftype, 'UILabel')
        pure_type_name = type_class.replace('UI', '')
        if ftype == 'tc':
            pure_type_name = 'Cell'
        self.ftype = ftype
        self.field_name = "{name}{type_name}".format(name=name, type_name=pure_type_name)
        self.name = name
        self.type_class = type_class
        self.constraints = dict((item.ctype, item.value) for item in constraints)
        self.attrs = dict((item.ctype, item.value) for item in attrs)
        self.in_vc = False

    @property
    def outlet(self):
        return '@IBOutlet weak var {field_name}:{type_class}!'.format(field_name=self.field_name,type_class=self.type_class)

    @property
    def has_value(self):
        return self.ftype in type_value_field_map

    @property
    def extract_value_stmt(self):
        if self.ftype == 'f':
            ctx = dict(name=self.name, field_name=self.field_name)
            stmt = 'let {name}Value = {field_name}.text?.strip()'.format(**ctx)
            ctx['value_type'] = self.value_type
            stmt += 'let field = BXField(name:"{name}",valueType:"{value_type}")\n'.format(**ctx)
            stmt += 'field.value = {name}Value\n'.format(name=self.name)
            stmt += 'fields.append(field)\n'
            return stmt

        else:
            return ''

    @property
    def set_value_stmt(self):
        if self.ftype in type_value_field_map:
            value_field = type_value_field_map.get(self.ftype, 'text')
            ctx = dict(name=self.name, field_name=self.field_name, value_field=value_field)
            return ' {field_name}.{value_field}  = model.{name} '.format(**ctx)
        else:
            return ''

    @property
    def is_required(self):
        return not self.attrs.get('empty', False)

    @property
    def check_value_stmt(self):
        if self.ftype in type_value_field_map and self.is_required:
            stmt = 'try Validators.checkText(typeValue)'
            return stmt
        else:
            return ''

    @property
    def can_set_value(self):
        return self.ftype in type_value_field_map

    @property
    def value_type(self):
        if self.has_value:
            return type_value_type_map[self.ftype]
        else:
            return ''


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

field_pattern = re.compile(r'(?P<fname>\w+)(?:\[(?P<constraints>[\w,]+)\])?(?:\((?P<attrs>[\w,]+)\))?')
model_pattern = re.compile(r'(?P<name>\w+)(?:\((?P<attrs>[\w=,]+)\))?')
int_value_pattern = re.compile(r'(?P<value>\d+)')

def parse_field_config(config):
    pairs = config.split(',') if config else []
    return [parse_field_config_item(pair) for pair in pairs]

def parse_field_info(field_info):
    parts = re.split(':', field_info.strip())
    field_config = parts[0]
    field_config = field_config.replace('"', '')
    matcher = field_pattern.match(field_config)
    groupdict = matcher.groupdict()
    fname = groupdict.get('fname').replace('-', '_')
    constraints_config = groupdict.get('constraints')
    constraints = parse_field_config(constraints_config)
    attrs_config = groupdict.get('attrs')
    attrs = parse_field_config(attrs_config)

    ftype = None
    if len(parts) > 1:
        ftype = parts[1]
    if not ftype:
        ftype = 'l'

    return UIField(fname, ftype, constraints, attrs)

def parse_line(line):
    field_infos = line.split(FIELD_DELIMETER)

    uifields = []
    for field_info in field_infos:
        field_info = field_info.strip()
        if not field_info:
            continue

        uifield = parse_field_info(field_info)
        if uifield:
            uifields.append(uifield)

    return uifields

outlet_tpl = '''
{% for comment in comments %}
    {{ comment }}
{% endfor %}

// MARK: Outlets
{% for field in uifields %}
  {{ field.outlet }}
{% endfor %}

    var allOutlets :[UIView]{
     return [{{ uifields|map(attribute='field_name')|join(',') }}]
    }
{% for grouper,fields in uifields|groupby('type_class') %}
    var all{{grouper}}Outlets :[{{grouper}}]{
        return [{{ fields|map(attribute='field_name')|join(',') }}]
    }
{% endfor %}

// MARK: Form
func extractFormValue() -> [BXField]{
 var fields = [BXField]()
 var field:BXField!
 {% for field in uifields %}
    {% if field.has_value %}
    // extract {{field.name}} Value
    let {{field.name}}Value = {{field.field_name}}.text?.strip()
    field = BXField(name:"{{field.name}}",valueType:"{{field.value_type}}")
    field.value = {{field.name}}Value
    fields.append(field)
    {% endif %}
 {% endfor %}
 return fields
}

func setFormValueWith(model:Model){
 {% for field in uifields %}
    {% if field.has_value %}
     {{field.set_value_stmt}}
    {% endif %}
 {% endfor %}
}

func checkValues(fields:[BXField]) throws{
 for field in fields {
    try Validators.checkField(field)
 }
}
'''


def main():
    uifield_list = []

    comments = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            comments.append("// " + line)
            uifields = parse_line(line)
            if uifields:
                uifield_list.extend(uifields)
    template = Template(outlet_tpl, trim_blocks=True, lstrip_blocks=True)
    # childViews = ','.join([f.field_name for f in uifield_list])
    text = template.render(uifields=uifield_list, comments=comments)
    print(text)


if __name__ == '__main__':
    main()