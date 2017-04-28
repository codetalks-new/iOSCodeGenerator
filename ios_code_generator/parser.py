# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from ios_code_generator.enviroment import ConstraintConfigItem, ConfigItem

__author__ = 'banxi'

from .utils import to_camel_case, to_mixed_case


FIELD_DELIMETER = ';'

''' match :`l>15@logo`,`l15`,`l25@logo` '''
constraint_config_item_pattern = re.compile(r"""
(?P<ctype>[a-zA-Z]+) # constraint keyword like: y
(?P<relation>[>=<])? # optional relation
(?P<value>\d+)? # optional value
(?:@(?P<secondItem>\w+))? # optional secondItem
""", re.VERBOSE)

''' match `f14`,`color=#fff`,'''
attr_config_item_pattern = re.compile(r"""
(?P<ctype>[a-zA-Z]+)  # attr name
(?:
    (?P<svalue>\d+) # simple number value
    |(?:\s*=\s*(?P<cvalue>[\w\u4e00-\u9fcc]+)) # normal value
)? # only name is allowed
""", re.VERBOSE)

field_pattern = re.compile(r"""
(?P<fname>\w+) # field name
\s* # optional space
(?:\[(?P<constraints>[\w@>=<,\s]+)\])? # optional constraints
\s* # optional space
(?:\((?P<attrs>[\w=,\u4e00-\u9fcc\s]+)\))? # optional attrs
""",re.VERBOSE)
model_pattern = re.compile(r'(?P<name>\w+)(?:\((?P<attrs>[\w=,/\s]+)\))?')
int_value_pattern = re.compile(r'(?P<value>\d+)')





class FieldParserMixin(object):
    default_field_type = 'l'
    @classmethod
    def parse_field_config_item(cls, config):
        c = config.strip()
        m = attr_config_item_pattern.match(c)
        groupdict = m.groupdict()
        simple_value = groupdict['svalue']
        complex_value = groupdict['cvalue']
        ctype = groupdict['ctype']
        return ConfigItem(ctype, simple_value, complex_value)

    @classmethod
    def parse_field_config(cls, config):
        pairs = config.split(',') if config else []
        return [cls.parse_field_config_item(pair) for pair in pairs if pair]

    @classmethod
    def parse_field_info(cls, field_info):
        parts = re.split(':', field_info.strip())
        field_config = parts[0]
        field_config = field_config.replace('"', '')

        ftype = parts[1] if len(parts) > 1 else cls.default_field_type

        matcher = field_pattern.match(field_config)
        groupdict = matcher.groupdict()
        fname = groupdict.get('fname').replace('-', '_')
        constraints_config = groupdict.get('constraints')
        attrs_config = groupdict.get('attrs')
        constraints = parse_constraint_config(constraints_config)
        attrs = cls.parse_field_config(attrs_config)

        return cls.field_class(fname, ftype, attrs, constraints=constraints)

    @classmethod
    def parse_field_line(cls, line):
        field_infos = re.split(r';', line)
        uifields = []
        for field_info in field_infos:
            field_info = field_info.strip()
            if not field_info:
                continue
            uifield = cls.parse_field_info(field_info)
            if uifield:
                uifields.append(uifield)

        return uifields

    @classmethod
    def parse_field_lines(cls, lines):
        fields = []
        for line in lines:
            field_list = cls.parse_field_line(line)
            fields.extend(field_list)
        return fields


class ModelParserMixin(FieldParserMixin):

        @classmethod
        def parse_model_line(cls, line):
            """解析一个模型容器声明"""
            model_info = line.split(FIELD_DELIMETER)[0]
            parts = re.split(':', model_info.strip())
            model_body = parts[0]
            if model_body[0] == '-':
                model_body = model_body[1:]
            mtype = parts[1] if len(parts) > 1 else 'v'
            matcher = model_pattern.search(model_body)
            raw_mname = matcher.groupdict().get('name')
            attrs_str = matcher.groupdict().get('attrs')
            model_name = to_camel_case(raw_mname)
            attr_pairs = attrs_str.split(',') if attrs_str else []
            config_items = [cls.parse_model_config_item(pair) for pair in attr_pairs if pair.strip()]
            return cls(model_name, mtype, config_items)

        @classmethod
        def parse_model_config_item(cls, config):
            c = config.strip()
            parts = c.split('=')
            ctype = parts[0]
            value = parts[1] if len(parts) > 1 else ctype
            return ConfigItem(ctype, value)

        @classmethod
        def parse_source(cls, lines):
            model = cls.parse_model_line(lines[0])
            field_lines = lines[1:]
            fields = cls.parse_field_lines(field_lines)
            model.fields = fields
            for field in fields:
                field.model = model
            return model, fields


def parse_constraint_config_item(config):
    c = config.strip()
    m = constraint_config_item_pattern.match(c)
    groupdict = m.groupdict()
    item = ConstraintConfigItem(**groupdict)
    return item


def parse_constraint_config(config):
    pairs = config.split(',') if config else []
    return [parse_constraint_config_item(pair) for pair in pairs if pair]







def parse_target_line(line):
    pairs = re.split(r'\s+',line)
    configs = dict()
    for pair in pairs:
        if '=' not in pair:
            configs[pair] = True
            continue
        key,value = pair.split('=')[0:2]
        configs[key]=value
    return configs

