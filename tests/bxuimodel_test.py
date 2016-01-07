#-*- coding:utf-8 -*-
import unittest

import os
import sys
sys.path.insert(0, os.path.basename('..'))
from io import StringIO

from ios_code_generator import bxuimodel
from ios_code_generator import bxuimodel_core as core

class MyTestCase(unittest.TestCase):
    def test_viewModel(self):
        strio = StringIO(u"-UserTableViewCell(m=User):tc\nauthor[y,l15,w36,a1]:i;bg[e0]:i;title(f14,cw);id[x,y](ch):l;url(cwa):b;mobile:f;bgView(cwa):v")
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
        text = core.generate('uicontroller')
        print(text)

    def test_enum(self):
        strio = StringIO(u"-User:s\nvideo;list;table;text;picture")
        sys.stdin = strio
        text = core.generate('enum')
        print(text)
        strio = StringIO(u"-User:i\nvideo;list;table;text;picture")
        sys.stdin = strio
        text = core.generate('enum')
        print(text)

    def test_enum_v2(self):
        strio = StringIO(u"-ExploreType:i\n curious:评测;news:菜谱;creator:维护;wiki:百科")
        sys.stdin = strio
        text = core.generate('enum')
        print(text)

    def test_const(self):
        strio = StringIO(u"-User\nvideo;list;table;text;picture")
        sys.stdin = strio
        text = core.generate('const')
        print(text)


if __name__ == '__main__':
    unittest.main()
