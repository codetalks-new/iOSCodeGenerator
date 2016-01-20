# -*- coding: utf-8 -*-
from __future__ import  unicode_literals
__author__ = 'banxi'

import re
import sys
from collections import namedtuple
from . import utils

FIELD_DELIMETER = ';'

ui_field_type_map = {
    'l': 'UILabel',
    'b': 'UIButton',
    'v': 'UIView',
    'i': 'UIImageView',
    'f': 'UITextField',
    't': 'UITableView',
    's': 'UIScrollView',
    'c': 'UICollectionView',
    'cr': 'UICollectionReusableView',
    'p': 'UIPickerView',
    'cb': 'CheckboxButton',
    'ib': 'IconButton',
    'sb': 'UISearchBar',
    'pc': 'UIPageControl',
    'dp': 'UIDatePicker',
    'st': 'UIStepper',
    'sw': 'UISwitch',
    'sl': 'UISlider',
    'sc': 'UISegmentedControl',
    'tc': 'UITableViewCell',
    'stc': 'StaticTableViewCell',
    'src': 'StarRatingControl',
    'tb': 'UIToolbar',
    'ctb': 'ConfirmTitleBar',
    'tv': 'UITextView',
    'il': 'IconLabel',
    'ci': 'OvalImageView',
    'wv': 'WKWebView',
    'gbb': 'GroupButtonBar',
    'oi': 'OutlineImageView'
}

ui_image_field_types = [
    'i','oi','ci'
]

ui_type_value_field_map = {
    'l': 'text',
    'f': 'text',
    'sw': 'on',
}

ui_type_value_type_map = {
    'l': 'String',
    'f': 'String',
    'sw': 'Bool'
}

### UIModel specifie
ui_view_designed_init_map = {
    'b': 'UIButton(type:.System)',
    'c': ' UICollectionView(frame: CGRectZero, collectionViewLayout: UICollectionViewFlowLayout())',
    'sb': 'UISearchBar()',
    'gbb': 'GroupButtonBar(buttons:[])'
}

ui_model_type_map = {
    'v': 'UIView',
    't': 'UITableView',
    's': 'UIScrollView',
    'c': 'UICollectionView',
    'tc': 'UITableViewCell',
    'stc': 'StaticTableViewCell',
    'cc': 'UICollectionViewCell',
    'vc': 'BaseUIViewController',
    'tvc': 'BaseUITableViewController',
    'tabvc': 'BaseUITabBarController',
}

ui_field_pin_map = {
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
    'hor': 'pinHorizontal',
    'ver': 'pinVertical',
}

ui_field_pa_map = {
    'x': 'pa_centerX',
    'y': 'pa_centerY',
    'l': 'pa_leading',
    't': 'pa_top',
    'r': 'pa_trailing',
    'b': 'pa_bottom',
    'w': 'pa_width',
    'h': 'pa_height',
    'a': 'pa_aspectRatio',
    'e': 'pac_edge',
    'hor': 'pac_horizontal',
    'ver': 'pac_vertical',
}
ui_vc_pin_map = {
    't': 'pinTopLayoutGuide',
    'b': 'pinBottomLayoutGuide'
}

ui_field_attr_map = {
    'f': 'UIFont.systemFontOfSize',
    'fb': 'UIFont.boldSystemFontOfSize',
    'cdg': 'UIColor.darkGrayColor',
    'cdt': 'UIColor.darkTextColor',
    'cdgt': '+AppColors.darkGrayTextColor',
    'cpt': '+AppColors.primaryTextColor',
    'cst': '+AppColors.secondaryTextColor',
    'ctt': '+AppColors.tertiaryTextColor',
    'cht': '+AppColors.hintTextColor',
    'cg': 'UIColor.grayColor',
    'clg': 'UIColor.lightGrayColor',
    'cb': 'UIColor.blackColor',
    'cw': 'UIColor.whiteColor',
    'cwa': '+UIColor(white: 1.0, alpha: 1.0)',
    'ch': '+UIColor(hex:0xabc)',
    'ca': '+AppColors.accentColor',
    'bp': 'setBackgroundImage(UIImage.Asset.ButtonPrimary.image,forState:.Normal)'
}

enum_raw_type_map = {
    'i': 'Int',
    's': 'String'
}

settings_raw_type_map = {
    'i':'Int',
    's':'String',
    'b': 'Bool',
    'f': 'Double',
    'u': 'NSURL',
    'd': 'NSDate',
}


# label:l,label2,button:b,view:v,imageView:i,field:f,addr:tc
def _to_camel_style(word):
    return word[0].upper() + word[1:]


def _to_camelCase_varName(word):
    return word[0].lower() + word[1:]


def _field_name_to_type_name(field_name):
    words = re.split('_', field_name)
    return ''.join([word for word in words if word])


class ModelDecl(object):
    def __init__(self, name, mtype, config_items):
        self.name = name
        self.mtype = mtype
        self.model_config = dict((item.ctype, item.value) for item in config_items)
        self.superclass = ui_model_type_map.get(mtype, 'UIView')

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
            'vname': self.vc_mname + "Cell"
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
        if 'vc' in self.mtype and 'ViewController' not in self.name:
            return self.name + 'ViewController'
        return self.name

    @property
    def prefix(self):
        return self.model_config.get('prefix','')



    ##################################
    ## Enum Support
    ##################################

    @property
    def raw_type(self):
        return enum_raw_type_map.get(self.mtype)

    ##### Defaults Support
    @property
    def settings_prefix(self):
        return self.prefix

    @property
    def settings_sync_on_save(self):
        value = self.model_config.get('sync_on_save','true').lower()
        if value in ['1','t','true','on']:
            return True
        return False


class UIField(object):
    def __init__(self, name, ftype, constraints, attrs):
        self.name = name
        self.ftype = ftype
        self.constraints = dict((item.ctype, item.value) for item in constraints)
        self.attrs = dict((item.ctype, item.value) for item in attrs)
        self.model = None
        self.in_vc = 'controller' in target


    @property
    def type_class(self):
        return ui_field_type_map.get(self.ftype, 'UILabel')

    @property
    def field_name(self):
        ''' deprecated '''
        return self.ui_field_name

    @property
    def ui_field_name(self):
        pure_type_name = self.type_class.replace('UI', '')
        if self.ftype == 'tc':
            pure_type_name = 'Cell'

        if self.name == '_':
            return utils.camelize(pure_type_name)
        else:
            if self.name.endswith('_'):
                return self.name[:-1]
            else:
                return  "{name}{type_name}".format(name=self.name, type_name=pure_type_name)

    @property
    def snake_name(self):
        return utils.snakelize(self.name)

    @property
    def camel_name(self):
       return utils.camelize(self.name)

    ### MARK: for Enum
    @property
    def enum_name(self):
        return self.snake_name

    @property
    def cap_name(self):
        # for Enum v1
        return self.snake_name

    @property
    def enum_title(self):
        return self.ftype

    ### MARK: For Settings

    @property
    def settings_name(self):
        return self.name

    @property
    def settings_key(self):
        prefix = self.model.prefix
        if prefix:
            return "%s_%s" % (prefix, self.name)
        else:
            return self.name

    @property
    def settings_type(self):
        return settings_raw_type_map.get(self.ftype,'String')

    @property
    def settings_type_annotation(self):
        t = self.settings_type
        if self.ftype in ['b','i','f']:
            return t
        else:
            return t+"?"

    @property
    def settings_setter_type(self):
        map = {
            'i':'Integer',
            'b':'Bool',
            'f':'Double',
            'u':'URL'
        }
        return map.get(self.ftype,'Object')

    @property
    def settings_getter_type(self):
        map = {
            'i':'integer',
            'b':'bool',
            'f':'double',
            'u':'URL',
            's':'string'
        }
        return map.get(self.ftype,'object')

    @property
    def settings_set_stmt(self):
        type = self.settings_setter_type
        key = 'Keys.%s' % self.settings_name
        return 'userDefaults.set%s(newValue,forKey:%s)' % (type,key)

    @property
    def settings_get_stmt(self):
        type = self.settings_getter_type
        key = 'Keys.%s' % self.settings_name
        stmt = 'return userDefaults.%sForKey(%s)' % (type,key)
        if self.ftype == 'd':
            stmt += " as? NSDate"
        return stmt

    @property
    def outlet(self):
        return '@IBOutlet weak var {field_name}:{type_class}!'.format(field_name=self.field_name,
                                                                      type_class=self.type_class)

    @property
    def has_value(self):
        return self.ftype in ui_type_value_field_map

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
        if self.ftype in ui_type_value_field_map:
            value_field = ui_type_value_field_map.get(self.ftype, 'text')
            ctx = dict(name=self.name, field_name=self.field_name, value_field=value_field)
            return ' {field_name}.{value_field}  = model.{name} '.format(**ctx)

        elif self.ftype == 'i':  # UIImage NSURL
            ctx = dict(name=self.name, field_name=self.field_name)
            return ' {field_name}.kf_setImageWithURL(item.{name})'.format(**ctx)

        else:
            return ''

    @property
    def is_required(self):
        return not self.attrs.get('empty', False)

    @property
    def check_value_stmt(self):
        if self.ftype in ui_type_value_field_map and self.is_required:
            stmt = 'try Validators.checkText(typeValue)'
            return stmt
        else:
            return ''

    @property
    def can_set_value(self):
        return self.ftype in ui_type_value_field_map

    @property
    def value_type(self):
        if self.has_value:
            return ui_type_value_type_map[self.ftype]
        else:
            return ''


            ################################################################################
            ## Above for outlet
            ## below for uimodel

    ################################################################################

    @property
    def can_bind_value(self):
        return self.has_value or self.ftype in ui_image_field_types  ## image can bind value

    @property
    def bind_value_stmt(self):
        if self.ftype in ui_type_value_field_map:
            value_field = ui_type_value_field_map.get(self.ftype, 'text')
            ctx = dict(name=self.name, field_name=self.field_name, value_field=value_field)
            return ' {field_name}.{value_field}  = item.{name} '.format(**ctx)
        elif self.ftype in ui_image_field_types:  # UIImage NSURL
            ctx = dict(name=self.name, field_name=self.field_name)
            return ' {field_name}.kf_setImageWithURL(item.{name})'.format(**ctx)
        else:
            return ''

    @property
    def declare_stmt(self):
        frame_init = '{type_class}(frame:CGRectZero)'.format(type_class=self.type_class)
        construct_exp = ui_view_designed_init_map.get(self.ftype, frame_init)
        stmt = ' let {field_name} = {construct_exp}'.format(field_name=self.field_name, construct_exp=construct_exp)
        if self.ftype == 'tc':
            stmt = '''
            lazy var {field_name} : UITableViewCell = '''.format(field_name=self.field_name)
            stmt += '''{
            let cell = UITableViewCell()
            return cell
            }()
            '''

        if self.ftype == 'c':
           stmt = ''' lazy var {field_name} :UICollectionView'''.format(field_name=self.field_name)
           stmt +=''' = { [unowned self] in
            return UICollectionView(frame: CGRectZero, collectionViewLayout: self.flowLayout)
      }()
            '''
           stmt += '''
  private lazy var flowLayout:UICollectionViewFlowLayout = {
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
            func_name = ui_field_pin_map.get(ctype)
            if func_name:
                complex_value = value
                if ctype == 'e':
                    complex_value = 'UIEdgeInsets(top: {value}, left: {value}, bottom: {value}, right: {value})'.format(
                        value=value)
                if self.in_vc and (ctype in ui_vc_pin_map):
                    ctx = dict(func_name=ui_vc_pin_map[ctype], view=self.field_name, value=complex_value)
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
        for ctype, value in self.attrs.iteritems():
            func_name = ui_field_attr_map.get(ctype)
            if not func_name:
                continue
            no_param = func_name.startswith('+')
            if no_param:
                func_name = func_name.replace('+', '')
            prop_name = 'font' if ctype.startswith('f') else 'textColor'
            if self.ftype == 'v':
                # UIView
                prop_name = 'backgroundColor'
            if ctype.startswith('b'):
                prop_name = ''  # UIButton property
            ctx = dict(field_name=self.field_name, prop_name=prop_name, func_name=func_name)
            if no_param:
                if self.ftype == 'b':
                    # UIButton
                    stmt = '{field_name}.setTitleColor({func_name}, forState: .Normal)'.format(**ctx)
                else:
                    stmt = '{field_name}.{prop_name} = {func_name}'.format(**ctx)
            else:
                ctx['value'] = value
                if self.ftype == 'b':
                    # UIButton
                    stmt = '{field_name}.setTitleColor({func_name}({value}), forState: .Normal)'.format(**ctx)
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
    return ConfigItem(ctype, value)


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


def generate(target='uimodel', **options):
    globals()['target'] = target
    print("// Build for target " + target)
    uifield_list = []
    comments = []
    last_model_decl = None
    for line in sys.stdin:
        line = line.strip()
        if line:
            if isinstance(line, str):
                line = line.decode(encoding='utf-8')
            comments.append("// " + line)
            if line.startswith('-'):
                last_model_decl = parse_model_name(line)
                continue
            uifields = parse_line(line)
            if uifields:
                uifield_list.extend(uifields)
    for field in uifield_list:
        field.model = last_model_decl
    from .helper import jinja2_env
    template = jinja2_env.get_template('bx%s_tpl.html' % target)
    has_textfield = len([field for field in uifield_list if field.ftype == 'f']) > 0
    text = template.render(model=last_model_decl, uifields=uifield_list, has_textfield=has_textfield, comments=comments)
    return text.encode('utf-8')
