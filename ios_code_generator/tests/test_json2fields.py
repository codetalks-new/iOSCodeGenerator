# -*- coding: utf-8 -*-
from StringIO import StringIO

import sys

from ios_code_generator.generators import json_to_fields

__author__ = 'banxi'

def test_json2fields():
    strio = StringIO(u"""
// this is a comment line
                "following": false,// test
                "allow_all_act_msg": false,
                "remark": "",
                "geo_enabled": true,
                "verified": false,
                "allow_all_comment": true
    """)
    sys.stdin = strio
    json_to_fields()

