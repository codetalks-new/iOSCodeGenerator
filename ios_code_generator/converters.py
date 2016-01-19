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
        text = text + '}'
    return json.loads(text)

def json_to_field_list(json_obj):
    return json_obj.keys()

def convert_text_to_field_list(text):
    json_obj = json_loads_object_fragment(text)
    return json_to_field_list(json_obj)