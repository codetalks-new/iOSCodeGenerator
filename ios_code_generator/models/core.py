# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections
from abc import ABCMeta, abstractmethod, abstractproperty

from ios_code_generator._compat import implements_to_string
from ios_code_generator._internal import _DictAccessorProperty
from ios_code_generator.parser import ModelParserMixin
from ios_code_generator.utils import cached_property, to_camel_case, to_mixed_case

__author__ = 'banxi'

@implements_to_string
class Field(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, ftype, attrs=None,**kwargs):
        self.name = name
        self.ftype = ftype
        if attrs:
            if isinstance(attrs, collections.Mapping):
                self.attrs = dict(attrs)
            else:
                self.attrs = {item.ctype: item for item in attrs}
        else:
            self.attrs = {}
        if not hasattr(self, 'model'):
            self.model = None

    def __str__(self):
        return u"%s:%s" % (self.name, self.ftype)

    @property
    def field_name(self):
        return to_mixed_case(self.name)

    @cached_property
    def camel_name(self):
        return to_camel_case(self.name)

    @cached_property
    def mixed_name(self):
        return to_mixed_case(self.name)

    @cached_property
    def setter_func_name(self):
        if self.name.endswith('?'):
            return self.name[:-1]
        return self.name


class model_property(_DictAccessorProperty):  # noqa
    def lookup(self, obj):
        return obj.model_config


class model_bool_property(object):
    def __init__(self, name_or_names):
        self.name_or_names = name_or_names

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        if isinstance(self.name_or_names, (list, tuple)):
            return any([name in obj.model_config for name in self.name_or_names])
        else:
            return self.name_or_names in obj.model_config


class target_property(_DictAccessorProperty):  # noqa
    def lookup(self, obj):
        return obj.target_config


@implements_to_string
class Model(ModelParserMixin, object):
    __metaclass__ = ABCMeta

    target = None # 输出目标 如 data_model, ui_model enum 等
    platform = "ios" # 输出目标平台
    lang = "swift" # 输出目标语言
    field_class = Field
    template = None
    prefix = model_property("prefix", default="")
    model_name = model_property('m', default='T')

    def __init__(self, name, mtype, config_items, fields=None):
        self.name = name
        self.mtype = mtype
        self.model_config = dict((item.ctype, item.value) for item in config_items)
        self.fields = fields
        self.target_config = dict()

    def __str__(self):
        return u"%s:%s" % (self.name, self.mtype)

    @cached_property
    def field_names(self):
        return [field.name for field in self.fields]

    def has_attr(self, attr):
        return attr in self.model_config

    @cached_property
    def camel_name(self):
        return to_camel_case(self.name)

    @cached_property
    def mixed_name(self):
        return  to_mixed_case(self.name)

    @property
    def mixed_model_name(self):
        return to_mixed_case(self.model_name)

    @property
    def class_name(self):
        return self.camel_name

    @classmethod
    def template_path(cls):
        if cls.template:
            return cls.template
        else:
            return "%s/%s/%s_tpl.html" % (cls.platform, cls.target, cls.lang)

    def template_context(self):
        return dict(
            model = self,
            fields = self.fields,
        )


