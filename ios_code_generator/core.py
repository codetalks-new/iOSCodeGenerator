# -*- coding: utf-8 -*-
from __future__ import  unicode_literals
from cached_property import  cached_property
from ios_code_generator.maps import ui_field_type_map, ui_image_field_types, ui_button_field_types, \
    ui_type_value_field_map, ui_type_value_type_map, ui_view_designed_init_map, ui_model_type_map, ui_field_attr_map, \
    enum_raw_type_map, settings_raw_type_map
from . import utils

__author__ = 'banxi'

### UIModel specifie


# label:l,label2,button:b,view:v,imageView:i,field:f,addr:tc
def _to_camel_style(word):
    return word[0].upper() + word[1:]


def _to_camelCase_varName(word):
    return word[0].lower() + word[1:]


class ModelDecl(object):
    def __init__(self, name, mtype, config_items):
        self.name = name
        self.mtype = mtype
        self.model_config = dict((item.ctype, item.value) for item in config_items)
        self.superclass = ui_model_type_map.get(mtype, 'UIView')
        self.fields = None

    def has_attr(self, attr):
        return attr in self.model_config

    @property
    def vc_mname(self):
        return self.model_config.get('m', 'T')

    @property
    def is_button_group(self):
        return self.mtype == 'button_group'


    @cached_property
    def ui_model_name(self):
        return self.model_config.get('m','T')

    @cached_property
    def ui_camel_mname(self):
        return utils.camelize_word(self.ui_model_name)

    @cached_property
    def ui_cell_name(self):
        if 'cell' in self.model_config:
            return self.model_config.get('cell')
        else:
            return self.ui_model_name+'Cell'

    @cached_property
    def ui_service_name(self):
        if 'service' in self.model_config:
            return self.ui_model_name+'Service'
        return ''

    @cached_property
    def ui_delegate_name(self):
        return utils.snakelize(self.name)+'Delegate'

    @property
    def camel_name(self):
        return utils.camelize(self.name)

    #####
    ### Main Feature Support (refesh,loadmore,page,detail)
    #######
    @cached_property
    def ui_has_detail(self):
        return 'detail' in self.model_config

    @cached_property
    def ui_has_refresh(self):
        return 'refresh' in self.model_config

    @cached_property
    def ui_has_loadmore(self):
        return 'loadmore' in self.model_config

    @cached_property
    def ui_has_page(self):
        if  'page' in self.model_config:
            return True
        return self.ui_has_loadmore

    @cached_property
    def ui_has_tab(self):
        return 'tab' in self.model_config

    @cached_property
    def ui_has_search(self):
        return 'search' in self.model_config

    @cached_property
    def ui_is_inline_search(self):
        return self.model_config.get('search','inline')

    @cached_property
    def has_req(self):
        if 'req' in self.model_config:
            return True
        return self.ui_has_loadmore or self.ui_has_page or self.ui_has_search or self.ui_has_refresh

    @cached_property
    def adapter_type(self):
        return self.model_config.get('adapter')

    @cached_property
    def has_adapter(self):
        return 'adapter' in self.model_config

    @cached_property
    def has_static_adapter(self):
        return 'sadapter' in self.model_config

    @property
    def adapter_decl(self):
        base = self.adapter_type
        if not base:
            return ''
        ctx = {
            'mname': self.ui_model_name,
            'vname': self.ui_cell_name
        }
        if base == 'c':
            return 'let adapter = SimpleGenericCollectionViewAdapter<{mname},{vname}>()'.format(**ctx)
        else:
            return 'let adapter = SimpleGenericTableViewAdapter<{mname},{vname}>()'.format(**ctx)

    @property
    def adapter_init(self):
        base = self.adapter_type
        if not base:
            return ''
        if base == 'c':
            return ' adapter.bindTo(collectionView)'
        else:
            return 'adapter.bindTo(tableView)'

    @cached_property
    def is_vc(self):
        return 'vc' in self.mtype

    @cached_property
    def is_tvc(self):
        return 'tvc' == self.mtype

    @cached_property
    def ui_is_lib(self):
        return 'lib' in self.model_config

    @cached_property
    def ui_no_bind(self):
        return 'nobind' in self.model_config

    @cached_property
    def ui_has_bind(self):
        return not self.ui_no_bind

    @property
    def class_name(self):
        if self.is_vc and 'Controller' not in self.name:
            return self.name + 'ViewController'
        return self.name

    def ui_vc_name_with(self,infix):
        suffix = infix + 'ViewController'
        if 'Controller' not in self.name:
            return self.name + infix
        if 'ViewController' in self.name:
            return self.name.replace('ViewController',suffix)
        return self.name.replace('Controller',suffix)

    #####
    ### Tab Feature
    ###
    @cached_property
    def ui_tab_vc_name(self):
        return self.ui_vc_name_with('Tab')

    @cached_property
    def ui_tab_type_name(self):
        if 'tab_type' in self.model_config:
            return self.model_config['tab_type']
        return self.ui_model_name+'Type'

    ######
    ### Detail Feature
    #####
    @cached_property
    def ui_detail_vc_name(self):
        return self.ui_vc_name_with('Detail')


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

    def create_env(self):
        from .enviroment import  Environment
        return  Environment(self,self.fields)

class UIField(object):
    def __init__(self, name, ftype, constraints, attrs):
        self.name = name
        self.ftype = ftype
        self.constraints = dict((item.ctype, item) for item in constraints)
        self.attrs = dict((item.ctype, item) for item in attrs)
        self.model = None

    @property
    def in_vc(self):
        if self.model:
            return self.model.is_vc
        return False

    @property
    def type_class(self):
        return ui_field_type_map.get(self.ftype, 'UILabel')

    @property
    def field_name(self):
        ''' deprecated '''
        return self.ui_field_name

    @property
    def ui_field_name(self):
        if self.model and self.model.is_button_group:
            return 'button'
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
        return settings_raw_type_map.get(self.ftype, 'String')

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
        env = self.model.create_env()
        return env.generate_install_constraint_stmts(self)


    @property
    def attrs_stmt(self):
        if not self.attrs:
            return ''
        stmts = []
        for ctype, item in self.attrs.iteritems():
            stmt = item.generate_bind_attr_value_stmt(self)
            if stmt:
                stmts.append(stmt)
        if stmts:
            text = '\n'.join(stmts)
            text += '\n'
            return text
        else:
            return ''

