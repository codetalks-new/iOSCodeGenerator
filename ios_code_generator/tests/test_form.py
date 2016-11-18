#-*- coding:utf-8 -*-

import sys

from io import StringIO

from ios_code_generator.generators import generate


def test_form():
    strio = StringIO(u"""
    UserEditor(m=User)
    _:c;label:l;name(required):f;button:b;view:v;imageView:i;field:f;addr:tc
    """)
    sys.stdin = strio
    output  = generate("form")
    print(output)

