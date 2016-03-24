#-*- coding:utf-8 -*-
from __future__ import  unicode_literals
import unittest

import os
import sys


sys.path.insert(0, os.path.basename('..'))
from io import StringIO

import ios_code_generator.generators
from ios_code_generator import bxuimodel
from ios_code_generator import bxuimodel_core as core

class MyTestCase(unittest.TestCase):
    def test_viewModel(self):
        strio = StringIO(u"-UserTableViewCell(m=User):tc\nauthor[y,l15,w36,a1](tint=ca):i;bg[e0]:i;title[bl8@author](f14,cw,text=我的);id[x,y](ch):l;url(cwa):b;mobile:f;bgView(cwa):v")
        sys.stdin = strio
        bxuimodel.main()

    def test_viewController(self):
        strio = StringIO(u'''
        -DiscoverViewController(m=DiscoverItem,req,adapter=c,page):vc
        slide[t0,hor0,h180]
        _[hor0,t0,b0]:c
        ''')
        # strio = StringIO(u"-User(m=ProductItem,req,adapter):tc\nauthor[y,l15,w36,a1]:i;bg[t,l,r,b]:i;title(f14,cw);id[x,y](ch):l;url(cwa):b;mobile:f;bgView(cwa):v")
        sys.stdin = strio
        text = ios_code_generator.generators.generate('uicontroller')
        print(text)

    def test_enum(self):
        strio = StringIO(u"-User:s\nvideo;list;table;text;picture")
        sys.stdin = strio
        text = ios_code_generator.generators.generate('enum')
        print(text)
        strio = StringIO(u"-User:i\nvideo;list;table;text;picture")
        sys.stdin = strio
        text = ios_code_generator.generators.generate('enum')
        print(text)

    def test_enum_v2(self):
        strio = StringIO(u"-ExploreType:i\n curious:评测;news:菜谱;creator:维护;wiki:百科")
        sys.stdin = strio
        text = ios_code_generator.generators.generate('enum')
        print(text)

    def test_const(self):
        strio = StringIO(u"-User\nvideo;list;table;text;picture")
        sys.stdin = strio
        text = ios_code_generator.generators.generate('const')
        print(text)

    def test_button_group(self):
        strio = StringIO("""
        -JobUserCell(m=JobUser):button_group
        view(f15,cst,text=录用):b
        """)
        sys.stdin = strio
        text = ios_code_generator.generators.generate('button_group')
        print(text)

    def test_sqlite_model(self):
        strio = StringIO("""
         -ClockRecord
        id:i;created:d;last_modified:d;clock_time:d;type:i;memo;props:j
        """)
        sys.stdin = strio
        text = ios_code_generator.generators.generate('sqlite_model')
        print(text)


if __name__ == '__main__':
    unittest.main()
