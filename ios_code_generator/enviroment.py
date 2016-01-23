# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.maps import *

__author__ = 'banxi'


class Environment(object):
    def __init__(self,model,fields):
        self.model = model
        self.fields = fields
        self.fields_map = dict((field.name,field) for field in fields)

    @property
    def in_vc(self):
        return self.model.is_vc

    def field_by_name(self,name):
        return self.fields_map.get(name)

    def generate_constraint_stmt(self,field,config):
        func_name = ui_field_pa_map.get(config.ctype)
        if not func_name:
            return None

        param_value = config.value_param_value
        if func_name.startswith('pac_'):
            # logoImageView.pac_horizontal(30)
            return '%s.%s(%s)' % (field.field_name, func_name,param_value)
        elif config.secondItem:
            anchor_field = self.field_by_name(config.secondItem)
            if config.is_relative_layout:
                # logoImageView.pa_below(titleLabel,offset:30)
                return '%s.%s(%s,offset:%s)%s' % (field.field_name,
                                                  func_name,anchor_field.field_name,param_value,config.relation_suffix)
            else:
                # logoImageView.pa_leading.eqTo(titleLabel).offset(30)
                return '%s.%s.%sTo(%s).offset(%s)' % (field.field_name,
                                                      func_name,config.relation_func_name, anchor_field.field_name,param_value)

        else:
            if self.in_vc and config.is_top_or_bottom:
                # logoImageView.pa_below(self.topLayoutGuide).offset(0)
                func = ui_vc_pa_func_map.get(config.ctype)
                return "%s.%s.offset(%s)%s" % (field.field_name,func, param_value,config.relation_suffix)
            else:
                value_comp = config.value_comp
                # logoImageView.pa_leading.eq(30)
                return '%s.%s%s%s' % (field.field_name, func_name,value_comp,config.relation_suffix)

    def generate_install_constraint_stmts(self,field):
        constraints = field.constraints
        if not constraints:
            return ''
        c_stmts = []
        for ctype, constraint in constraints.iteritems():
            stmt = self.generate_constraint_stmt(field,constraint)
            if stmt:
                c_stmts.append(stmt+".install()")
        if c_stmts:
            text = '\n'.join(c_stmts)
            text += '\n'
            return text
        else:
            return ''


class ConstraintConfigItem(object):
    """
     解析布局约束的配置 : l>15@name
    """
    def __init__(self,ctype='l',relation='eq',secondItem=None,value=None):
        self.ctype = ctype
        self.relation = relation if relation else '='
        self.secondItem = secondItem
        self.value = value if value else ''

    @property
    def is_top_or_bottom(self):
        return self.ctype in ['t','b']

    @property
    def relation_func_name(self):
        return ui_field_pa_relation_map.get(self.relation, 'eq')

    @property
    def relation_suffix(self):
        if self.relation == '>':
            return '.withGteRelation'
        elif self.relation == '<':
            return '.withLteRelation'
        else:
            return ''

    @property
    def value_comp(self):
        if not self.value:
            return ''
        func_name = self.relation_func_name
        return '.%s(%s)' % (func_name,self.value)

    @property
    def is_relative_layout(self):
        return self.ctype in ui_field_pa_relative_layout_map

    def anchor_name(self):
        if self.secondItem is not None:
            return self.secondItem

    def has_anchor(self):
        return self.secondItem is not None

    @property
    def value_param_value(self):
        if self.ctype == 'e':
            return 'UIEdgeInsets(top: {value}, left: {value}, bottom: {value}, right: {value})'.format( value=self.value)
        else:
            return self.value


class ConfigItem(object):
    '''Field 属性配置项 '''
    def __init__(self,ctype,value,complex_value=None):
        self.ctype = ctype
        self.value = value
        self.complex_value = complex_value

    @property
    def config_value(self):
        if self.value is not None:
            return self.value
        if self.complex_value is not None:
            cvalue = self.complex_value
            if cvalue.startswith('0x'):
                return '+UIColor(hex:%s)' % cvalue
            return self.complex_value
        return ''

    @property
    def value_comp(self):
        ## for cpt , return correspond colorValue
        func = ui_field_attr_map.get(self.ctype)
        if func and func[0] == '+':
            return func[1:]

        value = self.config_value
        if not value:
            return ''
        if value[0] == '+':
            return value[1:]
        if func:
                return '%s(%s)' % (func,value)
        else:
            # support color value sketch
            if value.startswith('c') and len(value) <= 4:
                color_value = ui_field_attr_map.get(value)
                if color_value.startswith('+'):
                    return color_value[1:]

            # support custom prop custom value
            return value

    def smart_prop_name(self,field):
        if self.ctype in ['f','fb']:
            return 'font'

        if self.ctype.startswith('c'):
            if field.ftype in ui_has_textColor_prop_field_types:
                return 'textColor'
            elif field.ftype in ui_prefer_tintColor_prop_field_types:
                return 'tintColor'
            else:
                return 'backgroundColor'
        if self.ctype in ui_field_attr_sketch_map:
            return ui_field_attr_sketch_map.get(self.ctype)
        else:
            # like text,and other custom prop
            if len(self.ctype) > 3:
                return self.ctype
            return ''

    def generate_bind_attr_value_stmt(self,field):
        prop_name = self.smart_prop_name(field)
        value_comp = self.value_comp
        ctx = dict(field_name=field.field_name, prop_name=prop_name, value = value_comp)
        bind_value_tpl = '{prop_name} = {value}'

        if prop_name == 'text':
            bind_value_tpl = '{prop_name} = "{value}"'

        if field.ftype in ui_button_field_types:
            if prop_name == 'textColor':
                bind_value_tpl = "setTitleColor({value},forState: .Normal)"
            if prop_name == 'font':
                bind_value_tpl = "titleLabel?.font = {value}"
            if prop_name == 'text':
                bind_value_tpl = 'setTitle("{value}",forState: .Normal)'
        tpl = "{field_name}."+bind_value_tpl
        return tpl.format(**ctx)

