# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.models import Field
from ios_code_generator.utils import cached_property, to_camel_case, to_mixed_case

__author__ = 'banxi'


class BaseDataField(Field):
    field_type_map = {}
    @cached_property
    def type_class(self):
        field_config = self.attrs.get('type')
        if field_config and field_config.config_value:
            return to_camel_case(field_config.config_value)
        if self.is_ref:
            return to_camel_case(self.name)
        else:
            if self.is_array:
                type_char = self.ftype[1]
                return self.field_type_map.get(type_char, 'String')
            else:
                return self.field_type_map.get(self.ftype,'String')

    @cached_property
    def field_type(self):
        if self.is_array:
            return '[%s]' % self.type_class
        else:
            return self.type_class

    @cached_property
    def is_array(self):
        return self.ftype[0] == '['

    @cached_property
    def is_date(self):
        return self.ftype == 'di'

    @cached_property
    def is_simple(self):
        return len(self.ftype) == 1

    @cached_property
    def is_complex(self):
        return len(self.ftype) > 1

    @cached_property
    def is_ref(self):
        return self.ftype == 'r' or self.ftype == '[r'

    @property
    def field_name(self):
        field_config = self.attrs.get('field')
        if field_config and field_config.config_value:
            return to_mixed_case(field_config.config_value)
        return super(BaseDataField, self).field_name