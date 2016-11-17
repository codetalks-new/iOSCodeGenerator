# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_ios_swift_generator
from .core import Model, model_property, model_bool_property
from ios_code_generator.models import Field

__author__ = 'banxi'

enum_raw_type_map = {
    'i': 'Int',
    's': 'String'
}


class EnumField(Field):
    """对于 Enum Field 来说,它的结构是名称标题的结构,如: home:主页"""
    @property
    def enum_title(self):
        return self.ftype


@as_ios_swift_generator("enum")
class EnumModel(Model):
    field_class = EnumField
    # 整型枚举的起始值
    start_value = model_property('start', default=0)
    has_icon = model_bool_property('icon')

    @property
    def raw_type(self):
        return enum_raw_type_map.get(self.mtype)

    @property
    def has_icon(self):
        return 'icon' in self.model_config

    @property
    def class_name(self):
        return self.camel_name
