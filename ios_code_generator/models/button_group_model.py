# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_ios_swift_generator
from ios_code_generator.maps import ui_field_type_map, ui_view_designed_init_map
from ios_code_generator.models import Model
from ios_code_generator.models.view_model import ViewField
from ios_code_generator.utils import cached_property
from ios_code_generator.utils import to_mixed_case

__author__ = 'banxi'

class ButtonField(ViewField):

    @property
    def field_name(self):
        return "button"

    @cached_property
    def type_class(self):
        return ui_field_type_map.get(self.ftype,'UIButton')

    @cached_property
    def button_name(self):
        return  to_mixed_case(self.name+'Button')

    @property
    def construct_exp(self):
        return  ui_view_designed_init_map.get(self.ftype, '%s()' % self.type_class)

@as_ios_swift_generator("button_group")
class ButtonGroupModel(Model):
    field_class = ButtonField


