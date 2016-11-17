# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from StringIO import StringIO

import sys

from ios_code_generator.generators import generate

__author__ = 'banxi'


def test_button_group():
    strio = StringIO("""
    -AccountCell(m=Account):button_group
    edit(title=设置库存):ob
    del(title=取消代理):ob
    update(title=取消代理):b
    """)
    sys.stdin = strio
    text = generate('button_group')
    print(text)