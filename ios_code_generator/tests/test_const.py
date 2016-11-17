# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from StringIO import StringIO

import sys

from ios_code_generator.generators import generate

__author__ = 'banxi'


def test_const():
    strio = StringIO(u"-User\nvideo;list;table;text;picture")
    sys.stdin = strio
    text = generate('const')
    print(text)