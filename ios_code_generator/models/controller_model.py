# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_ios_swift_generator
from ios_code_generator.maps import ui_model_type_map, ui_controller_model_type_map, ui_type_value_field_map
from ios_code_generator.models import model_bool_property
from ios_code_generator.models.view_model import ViewModel, ViewField
from ios_code_generator.utils import cached_property

__author__ = 'banxi'

class ControllerField(ViewField):
    @property
    def outlet(self):
        return '@IBOutlet weak var {field_name}:{type_class}!'.format(field_name=self.field_name,
                                                                      type_class=self.type_class)

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
    def is_required(self):
        return not self.attrs.get('empty', False)

    @property
    def check_value_stmt(self):
        if self.ftype in ui_type_value_field_map and self.is_required:
            stmt = 'try Validators.checkText(typeValue)'
            return stmt
        else:
            return ''

@as_ios_swift_generator("controller")
class ControllerModel(ViewModel):
    has_detail = model_bool_property("detail")
    has_refresh = model_bool_property("refresh")
    has_remove = model_bool_property("remove")
    has_loadmore = model_bool_property("loadmore")
    has_tab = model_bool_property("tab")
    has_search = model_bool_property("search")
    has_primary_action = model_bool_property(["paction","primary_action"]) # primary action
    has_keyboard = model_bool_property(["kb","keyboard"])
    has_search_ui = model_bool_property("search_ui")
    has_right_button = model_bool_property("right_button",default=False)
    init_views = model_bool_property("init_views", default=False)
    no_init = model_bool_property("no_init", default=True)
    is_vc = True

    @property
    def superclass(self):
        return  ui_controller_model_type_map.get(self.mtype, 'UIViewController')

    @cached_property
    def has_textfield(self):
        return any(f.ftype == 'f' for f in self.fields)

    @cached_property
    def is_tvc(self):
        return 'tvc' == self.mtype

    @cached_property
    def has_page(self):
        if 'page' in self.model_config:
            return True
        return self.has_loadmore

    @cached_property
    def is_inline_search(self):
        return self.model_config.get('search', 'inline')

    @cached_property
    def has_req(self):
        if 'req' in self.model_config:
            return True
        return self.has_loadmore or self.has_page or self.has_search or self.has_refresh

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
    def right_button_title(self):
        return self.model_config.get('right_button')