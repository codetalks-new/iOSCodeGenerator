# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'banxi'

try:
    import simplejson as json
except ImportError:
    import json


def json_loads_object_fragment(text):
    text = text.strip()
    if not text.startswith('{'):
        text = '{'+text
    if not text.endswith('}'):
        text += '}'
    return json.loads(text)

class JSONField(object):
    def __init__(self,name,value,index=0):
        self.name = name
        self.value = value
        self.index = index

    @property
    def guess_type(self):
        if isinstance(self.value,(str,unicode)) :
            if self.value.startswith('http'):return 'u'
            elif self.value.startswith('is'): return 'b'
        elif self.name in ['created']: return 'di'
        return ''

    def __str__(self):
        guess_type = self.guess_type
        if guess_type:
            return '%s:%s' % (self.name,guess_type)
        else:
            return self.name

def json_to_field_list(json_obj):
    return [JSONField(k, v) for k, v in json_obj.items()]

def convert_text_to_field_list(text):
    json_obj = json_loads_object_fragment(text)
    fields =  json_to_field_list(json_obj)
    for field in fields:
        field.index = text.find(field.name)
    return fields