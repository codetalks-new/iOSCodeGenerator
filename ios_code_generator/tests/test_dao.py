# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from StringIO import StringIO

import sys

__author__ = 'banxi'

from ios_code_generator.generators import generate

def test_dao1():
    strio = StringIO("""
         -ClockRecord
        id:i;created:d;last_modified:d;clock_time:d;type:i;memo;props:j
        """)
    sys.stdin = strio
    text = generate('dao')
    print(text)

def test_dao2():
    strio = StringIO("""
-MyDay
id;udid;group_id:i;date:di;memo;color;status:i;countdown_enabled:b;cover;pics;extras:j
        """)
    sys.stdin = strio
    text = generate('dao')
    print(text)