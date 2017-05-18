# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from StringIO import StringIO

import sys

from ios_code_generator.generators import generate_kotlin as generate
__author__ = 'banxi'

def test_base():
    strio = StringIO(u"-User\nid:i;nums:[i;url:[u;title;author:r;follows(type=Follow):[r;counts:[i;created:di;realname\n")
    sys.stdin = strio
    text = generate("model")
    print(text)