import unittest

import os
import sys
# sys.path.insert(0, os.path.basename('..'))
from io import StringIO

from ios_code_generator import bxuimodel
from ios_code_generator import bxuimodel_core as core

class MyTestCase(unittest.TestCase):
    def test_viewModel(self):
        strio = StringIO(u"-UserTableViewCell(m=User):tc\nauthor[y,l15,w36,a1]:i;bg[e0]:i;title(f14,cw);id[x,y](ch):l;url(cwa):b;mobile:f;bgView(cwa):v")
        sys.stdin = strio
        bxuimodel.main()

    def test_viewController(self):
        strio = StringIO(u"-User(m=ProductItem,req,adapter):tc\nauthor[y,l15,w36,a1]:i;bg[t,l,r,b]:i;title(f14,cw);id[x,y](ch):l;url(cwa):b;mobile:f;bgView(cwa):v")
        sys.stdin = strio
        text = core.generate('uicontroller')
        print(text)

    def test_enum(self):
        strio = StringIO(u"-User:s\nvideo;list;table;text;picture")
        sys.stdin = strio
        text = core.generate('enum')
        print(text)

if __name__ == '__main__':
    unittest.main()
