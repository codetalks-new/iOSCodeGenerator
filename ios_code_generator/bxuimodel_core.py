# -*- coding: utf-8 -*-
__author__ = 'banxi'

import re
import sys
from collections import namedtuple

FIELD_DELIMETER = ';'

char_type_map = {
    'l': 'UILabel',
    'b': 'UIButton',
    'v': 'UIView',
    'i': 'UIImageView',
    'f': 'UITextField',
    't': 'UITableView',
    'c': 'UICollectionView',
    'sb': 'UISearchBar',
    'pc': 'UIPageControl',
    'dp': 'UIDatePicker',
    'st': 'UIStepper',
    'sw': 'UISwitch',
    'sl': 'UISlide',
    'sc': 'UISegmentedControl',
    'tc': 'UITableViewCell',
    'tb': 'UIToolbar',
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


### UIModel specifie
view_designed_init_map = {
    'b': 'UIButton(type:.System)',
    'c': ' UICollectionView(frame: CGRectZero, collectionViewLayout: UICollectionViewFlowLayout())',
    'sb': 'UISearchBar()',
}

model_type_map = {
    'v': 'UIView',
    'tc': 'UITableViewCell',
    'cc': 'UICollectionViewCell',
    'vc': 'BaseUIViewController',
    'tvc': 'BaseUITableViewController',
    'tabvc': 'BaseUITabBarController',
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
    'a': 'pinAspectRatio',
    'e': 'pinEdge',

}

vc_pin_map = {
    't': 'pinTopLayoutGuide',
    'b': 'pinBottomLayoutGuide'
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
    'ch': '+UIColor(hex:0xabc)',
    'ca': '+AppColors.colorAccent',
}

enum_raw_type_map = {
    'i':'Int',
    's':'String'
}
# label:l,label2,button:b,view:v,imageView:i,field:f,addr:tc
def _to_camel_style(word):
    return word[0].uppercase() + word[1:]

def _field_name_to_type_name(field_name):
    words = re.split('_', field_name)
    return ''.join([word for word in words if word])

class ModelDecl(object):
    def __init__(self, name, mtype, config_items):
        self.name = name
        self.mtype = mtype
        self.model_config = dict((item.ctype,item.value) for item in config_items)
        self.superclass = model_type_map.get(mtype, 'UIView')

    def has_attr(self, attr):
        return attr in self.model_config

    @property
    def vc_mname(self):
        return self.model_config.get('m', 'T')

    @property
    def has_adapter(self):
        return 'adapter' in self.model_config

    @property
    def adapter_decl(self):
        base = self.model_config.get('adapter')
        if not base:
            return ''
        ctx = {
            'mname': self.vc_mname,
            'vname': self.vc_mname+"Cell"
        }
        if base == 'c':
            return 'var adapter:SimpleGenericCollectionViewAdapter<{mname},{vname}>!'.format(**ctx)
        else:
            return 'var adapter:SimpleGenericTableViewAdapter<{mname},{vname}>!'.format(**ctx)

    @property
    def adapter_init(self):
        base = self.model_config.get('adapter')
        if not base:
            return ''
        if base == 'c':
            return ' adapter = SimpleGenericCollectionViewAdapter(collectionView:collectionView)'
        else:
            return 'adapter = SimpleGenericTableViewAdapter(tableView:tableView)'

    @property
    def is_vc(self):
        return 'vc' in self.mtype

    @property
    def is_tvc(self):
        return 'tvc' == self.mtype

    @property
    def class_name(self):
        if 'vc' in self.mtype:
            return self.name + 'ViewController'
        return self.name

    ##################################
    ## Enum Support
    ##################################

    @property
    def raw_type(self):
        return enum_raw_type_map.get(self.mtype)


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
        self.in_vc = 'controller' in target

    @property
    def cap_name(self):
        return self.name.capitalize()

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

        elif self.ftype == 'i': #UIImage NSURL
            ctx = dict(name=self.name, field_name=self.field_name)
            return ' {field_name}.kf_setImageWithURL(item.{name})'.format(**ctx)

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


   ################################################################################
        ## Above for outlet
        ## below for uimodel
    ################################################################################

    @property
    def can_bind_value(self):
        return self.has_value or self.ftype in ['i'] ## image can bind value

    @property
    def bind_value_stmt(self):
        if self.ftype in type_value_field_map:
            value_field = type_value_field_map.get(self.ftype, 'text')
            ctx = dict(name=self.name, field_name=self.field_name, value_field=value_field)
            return ' {field_name}.{value_field}  = item.{name} '.format(**ctx)
        elif self.ftype == 'i': #UIImage NSURL
            ctx = dict(name=self.name, field_name=self.field_name)
            return ' {field_name}.kf_setImageWithURL(item.{name})'.format(**ctx)
        else:
            return ''

    @property
    def declare_stmt(self):
        frame_init = '{type_class}(frame:CGRectZero)'.format(type_class=self.type_class)
        construct_exp = view_designed_init_map.get(self.ftype, frame_init)
        stmt = ' let {field_name} = {construct_exp}'.format(field_name=self.field_name, construct_exp=construct_exp)
        if self.ftype == 'c':
            stmt += '''
  private let flowLayout:UICollectionViewFlowLayout = {
      let flowLayout = UICollectionViewFlowLayout()
      flowLayout.minimumInteritemSpacing = 10
      flowLayout.itemSize = CGSize(width:100,height:100)
      flowLayout.minimumLineSpacing = 0
      flowLayout.sectionInset = UIEdgeInsetsZero
      flowLayout.scrollDirection = .Vertical
      return flowLayout
  }()
            '''

        return stmt

    @property
    def constraints_stmt(self):
        if not self.constraints:
            return ''
        c_stmts = []

        for ctype, value in self.constraints.iteritems():
            func_name = field_pin_map.get(ctype)
            if func_name:
                complex_value = value
                if ctype == 'e':
                    complex_value = 'UIEdgeInsts(top: {value}, left: {value}, bottom: {value}, right: {value})'.format(value=value)
                if self.in_vc and (ctype in vc_pin_map):
                    ctx = dict(func_name=vc_pin_map[ctype], view=self.field_name, value=complex_value)
                    stmt = '{func_name}({view},margin:{value})'.format(**ctx)
                else:
                    ctx = dict(field_name=self.field_name, func_name=func_name, value=complex_value)
                    stmt = '{field_name}.{func_name}({value})'.format(**ctx)
                c_stmts.append(stmt)
        if c_stmts:
            c_stmts.append('')
        return '\n'.join(c_stmts)

    @property
    def attrs_stmt(self):
        if not self.attrs:
            return ''
        stmts = []
        for ctype,value in self.attrs.iteritems():
            func_name = field_attr_map.get(ctype)
            if not func_name:
                continue
            no_param = func_name.startswith('+')
            if no_param:
                func_name = func_name.replace('+', '')
            prop_name = 'font' if ctype.startswith('f') else 'textColor'
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
                ctx['value'] = value
                if self.ftype == 'b':
                    # UIButton
                    stmt = '{field_name}.setTitleColor({func_name}({value}), forState: .Normal)' .format(**ctx)
                else:
                    stmt = '{field_name}.{prop_name} = {func_name}({value})'.format(**ctx)
            stmts.append(stmt)

        return '\n'.join(stmts)


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


def parse_model_config_item(config):
    c = config.strip()
    parts = c.split('=')
    ctype = parts[0]
    value = parts[1] if len(parts) > 1 else ctype
    return ConfigItem(ctype,value)

def parse_model_name(line):
    model_info = line.split(FIELD_DELIMETER)[0]
    parts = re.split(':', model_info.strip())
    model_config = parts[0][1:]  # drop leading '-'
    mtype = parts[1] if len(parts) > 1 else 'v'
    matcher = model_pattern.search(model_config)
    raw_mname = matcher.groupdict().get('name')
    attrs_str = matcher.groupdict().get('attrs')
    model_name = _field_name_to_type_name(raw_mname)
    attr_pairs = attrs_str.split(',') if attrs_str else []
    config_items = [parse_model_config_item(pair) for pair in attr_pairs if pair.strip()]
    return ModelDecl(model_name, mtype, config_items)


def parse_line(line):
    field_infos = re.split(r';', line)
    uifields = []
    for field_info in field_infos:
        field_info = field_info.strip()
        if not field_info:
            continue
        uifield = parse_field_info(field_info)
        if uifield:
            uifields.append(uifield)

    return uifields


target = 'uimodel'
def generate(target='uimodel',  **options):
    globals()['target'] = target
    print("// Build for target "+target)
    uifield_list = []
    comments = []
    last_model_decl = None
    for line in sys.stdin:
        line = line.strip()
        if line:
            comments.append("// " + line)
            if line.startswith('-'):
                last_model_decl = parse_model_name(line)
                continue
            uifields = parse_line(line)
            if uifields:
                uifield_list.extend(uifields)
    from .helper import jinja2_env
    template = jinja2_env.get_template('bx%s_tpl.html' % target)
    has_textfield = len([field for field in uifield_list if field.ftype == 'f' ]) > 0
    return template.render(model=last_model_decl, uifields=uifield_list, has_textfield=has_textfield, comments=comments)


