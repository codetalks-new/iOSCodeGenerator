# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_ios_swift_generator
from ios_code_generator.maps import m_char_type_map
from ios_code_generator.models import Model
from ios_code_generator.models import model_bool_property
from ios_code_generator.models.base_data_model import BaseDataField
from ios_code_generator.utils import cached_property

__author__ = 'banxi'


class DataField(BaseDataField):
    field_type_map = m_char_type_map

    @property
    def declare_stmt(self):
        stmt =  'let {field_name} : {field_type}'.format(field_name=self.field_name, field_type=self.field_type)
        return stmt

    @property
    def init_stmt(self):
        from string import Template
        ctx = {
            'name': self.name,
            'field_name': self.field_name,
            'type_class': self.type_class
        }
        tpl = "self.$field_name = "
        if self.is_complex:
            if self.is_array:
                type_char = self.ftype[1]
                if type_char == 'r':
                    tpl += '$type_class.arrayFrom(json["$name"])'
                elif type_char == 'u':
                    tpl += 'json["$name"].flatMap{ $$1.URL } '
                else:
                    tpl += 'json["$name"].arrayObject as? [$type_class] ?? []'
            else:
                if self.is_date:
                    if  self.ftype == "di":
                        tmp_value_stmt = 'let tmp_{name}_value = json["{name}"].{json_type}Value '\
                            .format(name=self.name, json_type="double")
                        tpl = tmp_value_stmt + "\n" + tpl
                        tpl += 'Date(timeIntervalSince1970: tmp_${name}_value)'
                    elif self.ftype == "ds":
                        tpl += 'json["{name}"].stringValue.dateFromISO8601'.format(name=self.name)
                elif self.is_enum:
                    if self.ftype == "ei":
                        tpl += '$type_class(rawValue:json["$name"].intValue)'
                    elif self.ftype == "es":
                        tpl += '$type_class(rawValue:json["$name"].stringValue)'

        else:
            if self.ftype == 'r':
                tpl += '$type_class(json:json["$name"])'

            elif self.ftype == 'u':
                tpl += ' json["$name"].url'
            elif self.ftype == 'j':
                tpl += ' json["$name"]'
            else:
                json_type = ctx['type_class'].lower()
                ctx['json_type'] = json_type
                tpl += ' json["$name"].${json_type}Value'

        stmt =  Template(tpl).safe_substitute(**ctx)
        return stmt

    @cached_property
    def to_dict_stmt(self):
        from string import Template
        tpl = 'dict["$name"] = self.$field_name'
        if self.is_complex:
            if self.is_array:
                tpl += ".map{ $0.toDict() }"
            else:
                if self.is_date:
                    if self.ftype == "di":
                        tpl += ".timeIntervalSince1970"
                    elif self.ftype == "ds":
                        tpl += '?.iso8601'
                elif self.is_enum:
                    tpl += ".rawValue"

        else:
            if self.ftype == 'r':
                tpl += ".toDict()"
            elif self.ftype == 'u':
                tpl += "?.absoluteString"
            elif self.ftype == 'j':
                tpl += ".object"

        return Template(tpl).safe_substitute(name=self.name, field_name=self.field_name)


@as_ios_swift_generator("model")
class DataModel(Model):
    default_field_type = 's'
    field_class = DataField
    impl_eq = model_bool_property('eq')
    impl_hash = model_bool_property('hash')
    impl_tos = True # better to be default model_bool_property(['tos, ts'])
    is_class = model_bool_property(['c','class'])

    is_public = model_bool_property(['public'])
    is_open = model_bool_property(['open'])


    @cached_property
    def access_level_modifier(self):
        if self.is_open:
            return "open "
        if self.is_public:
            return "public "
        return ""


    @cached_property
    def identifier_field_name(self):
        for name in ['_id', 'id', 'code']:
            if name in self.field_names:
                return name
        for name in self.field_names:
            if name.endswith("id"):
                return name
        return ""

    @cached_property
    def has_id(self):
        if not self.fields:return False
        for f in self.fields:
            if f.name == 'id': return True
        return False

    def guess_tos_field_name(self):
        for name in ['name', 'title', 'desc']:
            if name in self.field_names:
                return name
        return ""



