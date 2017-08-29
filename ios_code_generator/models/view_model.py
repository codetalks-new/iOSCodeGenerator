# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_ios_swift_generator
from ios_code_generator.maps import ui_field_custom_type_pure_name, ui_field_type_map, ui_type_value_field_map, \
    ui_image_field_types, ui_view_designed_init_map, ui_type_value_type_map, ui_model_type_map
from ios_code_generator.models import Model, Field
from ios_code_generator.models import model_bool_property
from ios_code_generator.utils import to_mixed_case, cached_property, to_camel_case

__author__ = 'banxi'

class ViewField(Field):

    def __init__(self, name, ftype, attrs=None,**kwargs):
        constraints = kwargs.pop('constraints', [])
        self.constraints = {item.ctype: item for item in constraints}
        super(ViewField, self).__init__(name, ftype, attrs=attrs, **kwargs)

    @cached_property
    def type_class(self):
        return ui_field_type_map.get(self.ftype,'UIView')

    @property
    def field_name(self):

        pure_type_name = self.type_class.replace('UI', '')
        if not self.type_class.startswith("UI"):
            if self.ftype in ui_field_custom_type_pure_name:
                pure_type_name = ui_field_custom_type_pure_name.get(self.ftype)
        if pure_type_name.endswith('Cell'):
            pure_type_name = 'Cell'

        if self.name == '_':
            return to_mixed_case(pure_type_name)
        else:
            if self.name.endswith('_'):
                return self.name[:-1]
            else:
                return  "{name}{type_name}".format(name=self.name, type_name=pure_type_name)



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
            return ' {field_name}.kf.setImage(with: item.{name})'.format(**ctx)
        else:
            return ''

    @property
    def declare_stmt(self):
        frame_init = '{type_class}(frame:.zero)'.format(type_class=self.type_class)
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
            stmt += ''' = { [unowned self] in
              return UICollectionView(frame: .zero, collectionViewLayout: self.flowLayout)
        }()
              '''
            stmt += '''
    private lazy var flowLayout:UICollectionViewFlowLayout = {
        let flowLayout = UICollectionViewFlowLayout()
        flowLayout.minimumInteritemSpacing = 10
        flowLayout.itemSize = CGSize(width:100,height:100)
        flowLayout.minimumLineSpacing = 0
        flowLayout.sectionInset = .zero
        flowLayout.scrollDirection = .vertical
        return flowLayout
    }()
              '''

        return stmt

    @cached_property
    def constraints_stmt(self):
        env = self.model.create_env()
        try:
            return env.generate_install_constraint_stmts(self)
        except Exception as e:
            return e.message

    @cached_property
    def attrs_stmt(self):
        if not self.attrs:
            return ''
        stmts = []
        for ctype, item in self.attrs.items():
            try:
                stmt = item.generate_bind_attr_value_stmt(self)
            except Exception as e:
                stmt = e.message
            if stmt:
                stmts.append(stmt)
        if stmts:
            text = '\n'.join(stmts)
            return text
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
            return ' {field_name}.kf.setImage(with: item.{name})'.format(**ctx)

        else:
            return ''

    @property
    def has_value(self):
        return self.ftype in ui_type_value_field_map

    @property
    def can_set_value(self):
        return self.ftype in ui_type_value_field_map

    @property
    def value_type(self):
        if self.has_value:
            return ui_type_value_type_map[self.ftype]
        else:
            return ''


@as_ios_swift_generator("view")
class ViewModel(Model):
    default_field_type = 'l'
    field_class = ViewField
    is_autolayout = model_bool_property(['al', 'autolayout'])
    has_adapter = model_bool_property('adapter')
    has_static_adapter = model_bool_property('sadapter')
    no_init = model_bool_property("no_init")
    is_vc = False
    @property
    def superclass(self):
        return  ui_model_type_map.get(self.mtype, 'UIView')

    def create_env(self):
        from ios_code_generator.enviroment import  Environment
        return  Environment(self,self.fields)


    @property
    def is_button_group(self):
        return self.mtype == 'button_group'


    @cached_property
    def ui_model_name(self):
        return self.model_name

    @cached_property
    def ui_model_field_name(self):
        return to_mixed_case(self.ui_model_name)

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
        return to_camel_case(self.name) + 'Delegate'

    @cached_property
    def adapter_type(self):
        return self.model_config.get('adapter')


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
            return 'let adapter = SimpleCollectionViewAdapter<{mname},{vname}>()'.format(**ctx)
        else:
            return 'let adapter = SimpleTableViewAdapter<{mname},{vname}>()'.format(**ctx)

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
    def ui_is_lib(self):
        return 'lib' in self.model_config

    @cached_property
    def ui_no_bind(self):
        return  'm' not in self.model_config

    @cached_property
    def ui_has_bind(self):
        return not self.ui_no_bind
