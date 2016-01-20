# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'banxi'

import re
from collections import namedtuple
import functools
from .core import  *
from . import utils


constraint_config_valid_chars_re=r'[a-zA-Z0-9_@>=<]'

''' match :`l>15@logo`,`l15`,`l25@logo` '''
constraint_config_item_pattern = re.compile(r'(?P<ctype>[a-zA-Z]+)(?P<relation>[>=<])?(?P<value>\d+)(?:@(?P<secondItem>\w+))?')
''' match `f14`,`color=#fff`,'''
attr_config_item_pattern = re.compile(r'(?P<ctype>[a-zA-Z]+)(?:(?P<svalue>\d+)|(?:=(?P<cvalue>#?[\w]+)))?')

field_pattern = re.compile(r'(?P<fname>\w+)(?:\[(?P<constraints>[\w@>=<,]+)\])?(?:\((?P<attrs>[\w=#,]+)\))?')
model_pattern = re.compile(r'(?P<name>\w+)(?:\((?P<attrs>[\w=,]+)\))?')
int_value_pattern = re.compile(r'(?P<value>\d+)')


ConfigItem = namedtuple('ConfigItem', ['ctype', 'value'])

class ConstraintConfigItem(object):
    """
     解析布局约束的配置 : l>15@name
    """
    def __init__(self,ctype='l',relation='eq',secondItem=None,value=0):
        self.ctype = ctype
        self.relation = relation
        self.secondItem = secondItem
        self.value = value

def parse_constraint_config_item(config):
    c = config.strip()
    m = constraint_config_item_pattern.match(c)
    groupdict = m.groupdict()
    if groupdict['relation'] is None:
        groupdict['relation'] = 'eq'
    item = ConstraintConfigItem(**groupdict)
    return item


class ConfigItem(object):
    '''Field 属性配置项 '''
    def __init__(self,ctype,value,complex_value=None):
        self.ctype = ctype
        self.value = value
        self.complex_value = complex_value


def parse_field_config_item(config):
    c = config.strip()
    m = attr_config_item_pattern.match(c)
    groupdict = m.groupdict()
    simple_value = groupdict['svalue']
    complex_value = groupdict['cvalue']
    ctype = groupdict['ctype']
    return ConfigItem(ctype, simple_value,complex_value)





def parse_field_config(config):
    pairs = config.split(',') if config else []
    return [parse_field_config_item(pair) for pair in pairs]


def parse_field_info(field_info):
    parts = re.split(':', field_info.strip())
    field_config = parts[0]
    field_config = field_config.replace('"', '')

    ftype = parts[1] if len(parts) > 1 else 'l'

    matcher = field_pattern.match(field_config)
    groupdict = matcher.groupdict()
    fname = groupdict.get('fname').replace('-', '_')
    constraints_config = groupdict.get('constraints')
    constraints = parse_field_config(constraints_config)
    attrs_config = groupdict.get('attrs')
    attrs = parse_field_config(attrs_config)

    return UIField(fname, ftype, constraints, attrs)


def parse_model_config_item(config):
    c = config.strip()
    parts = c.split('=')
    ctype = parts[0]
    value = parts[1] if len(parts) > 1 else ctype
    return ConfigItem(ctype, value)


def parse_model(line):
    """解析一个模型容器声明"""
    model_info = line.split(FIELD_DELIMETER)[0]
    parts = re.split(':', model_info.strip())
    model_config = parts[0][1:]  # drop leading '-'
    mtype = parts[1] if len(parts) > 1 else 'v'
    matcher = model_pattern.search(model_config)
    raw_mname = matcher.groupdict().get('name')
    attrs_str = matcher.groupdict().get('attrs')
    model_name = utils.snakelize(raw_mname)
    attr_pairs = attrs_str.split(',') if attrs_str else []
    config_items = [parse_model_config_item(pair) for pair in attr_pairs if pair.strip()]
    return ModelDecl(model_name, mtype, config_items)


def parse_line(line):
    field_infos = re.split(r';', line)
    uifields = []
    for field_info in field_infos:
        field_info = field_info.strip()
        if not field_info:
            continue
        uifield = parse_field_info(field_info)
        if uifield:
            uifields.append(uifield)

    return uifields

def parse_lines(lines):
    fields = []
    for line in lines:
       field_list = parse_line(line)
       fields.extend(field_list)
    return fields

def parse_source(lines):
    model = parse_model(lines[0])
    fields = parse_lines(lines)
    return model,fields

