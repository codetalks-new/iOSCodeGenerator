# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections
from abc import ABCMeta, abstractmethod, abstractproperty

from ios_code_generator._compat import implements_to_string
from ios_code_generator._internal import _DictAccessorProperty
from ios_code_generator.parser import ModelParserMixin
from ios_code_generator.utils import cached_property, to_camel_case, to_mixed_case

"""
速写代码
主要通过 Model-Field 来构造生成代码。
Model 控制代码的主要结构， Field 控制一些具体项的生成细节。
最开始主要是为了通过生成 MVC 中的数据模型代码。

"""
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

    @cached_property
    def field_name(self):
        name = self.name
        if self.name.endswith('?'):
            name = self.name[:-1]
        return to_mixed_case(name)

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
    """
    用于 Model 类的属性 Descriptor,依赖 `model_config` 字段。
    用于读取属性值和提供默认值。
    """
    def lookup(self, obj):
        return obj.model_config



class model_bool_property(object):
    """
    用于 Model 类的属性 Descriptor,依赖 `model_config` 字段。
    直接通过提供开关名作为指令标志。如 `eq` 表示 开关值为真， `eq=false` 表示开关值为假
    """

    def __init__(self, name_or_names, default = False):
        """
        :param name_or_names: 单个名称或名称列表，列表主要是为了支持缩写
        :param default: 开关默认值 False
        """
        self.name_or_names = name_or_names
        self.default = default

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        config_value = self.default
        false_literals = ['false','no']
        if isinstance(self.name_or_names, (list, tuple)):
            for name in self.name_or_names:
                if name in obj.model_config:
                    config_value = obj.model_config[name] not in false_literals
        else:
            if self.name_or_names in obj.model_config:
                config_value = obj.model_config[self.name_or_names] not in false_literals
        return  config_value


class target_property(_DictAccessorProperty):  # noqa
    def lookup(self, obj):
        return obj.target_config


@implements_to_string
class Model(ModelParserMixin, object):
    __metaclass__ = ABCMeta

    target = None # 输出目标 如 data_model, ui_model enum 等
    platform = "ios" # 输出目标平台
    lang = "swift" # 输出目标语言
    field_class = Field # 对应的字段类
    template = None # 默认模板路径
    prefix = model_property("prefix", default="") # 前缀
    model_name = model_property('m', default='T') # 模型名，
    FRAGMENT_NAME = '_FRAGMENT_'

    def __init__(self, name, mtype='', config_items=None, fields=None):
        config_items = config_items or []
        self.name = name
        self.mtype = mtype
        self.model_config = dict((item.ctype, item.value) for item in config_items)
        self.fields = fields
        self.target_config = dict()

    @property
    def is_fragment(self):
        return self.name == '_FRAGMENT_'

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
        """
        要生成的代码模板的路径,如果 `template` 字段不为空，则返回 `template`
        否则按规则拼接对应的路径。
        :return:  模板路径
        """
        if cls.template:
            return cls.template
        else:
            return "%s/%s/%s_tpl.html" % (cls.platform, cls.target, cls.lang)

    def template_context(self):
        """
        默认的上下文包括,`model`, 和 `fields`
        :return: 模板渲染的上下文
        """
        return dict(
            model = self,
            fields = self.fields,
        )


