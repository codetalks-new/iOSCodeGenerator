# -*- coding: utf-8 -*-
from StringIO import StringIO

import sys

from ios_code_generator import utils
from ios_code_generator.generators import json_to_fields, json_escape_quote, json_remove_comment

__author__ = 'banxi'

def test_json2fields():
    strio = StringIO(u"""
"no": "qc1",
"category": "汽 ",
"name": "兰博基尼  ",
"price": 7388800,
"stock": 1,
"tp": 8127680,
"level": 100,
"picture": ""
    """)
    sys.stdin = strio
    json_to_fields()

def test_json_remove_comments():
    text = u"""

    """

    in_lines = text.splitlines()
    lines = json_remove_comment(in_lines)
    ouput_text = "\n".join(lines)
    print(ouput_text)

def test_json_escape_quote():
    strio = StringIO(u"""

        """)
    sys.stdin = strio
    lines = utils.readlines_from_stdin()
    output_lines = json_escape_quote(lines)
    text = "".join(output_lines)
    print(text)

