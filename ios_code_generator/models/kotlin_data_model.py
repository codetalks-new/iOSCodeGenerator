# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_android_kotlin_generator
from ios_code_generator.maps import m_kotlin_char_type_map
from ios_code_generator.models import  Model
from ios_code_generator.models.base_data_model import BaseDataField
from ios_code_generator.utils import cached_property

__author__ = 'banxi'

class KotlinDataField(BaseDataField):
    field_type_map = m_kotlin_char_type_map
    @cached_property
    def field_type(self):
        if self.is_array:
            return 'Array<%s>' % self.type_class
        else:
            return self.type_class


@as_android_kotlin_generator('model')
class KotlinDataModel(Model):
    default_field_type = 's'
    field_class = KotlinDataField