# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import functools
from StringIO import StringIO

import sys

from ios_code_generator.generators import generate, generate_kotlin

generate_enum = functools.partial(generate,'enum')
__author__ = 'banxi'


def test_enum():
    strio = StringIO(u"-User:s\nvideo;list;table;text;picture")
    sys.stdin = strio
    text = generate_enum()
    print(text)

def test_kotlin_enum():
    strio = StringIO(u"-User:s\nvideo;list;table;text;picture")
    sys.stdin = strio
    text = generate_kotlin('enum')
    print(text)

def test_enum_v2():
    strio = StringIO(u"-ExploreType:i\n curious:评测;news:菜谱;creator:维护;wiki:百科")
    sys.stdin = strio
    text = generate_enum()
    print(text)