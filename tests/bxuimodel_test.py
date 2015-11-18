import unittest

import bxuimodel
import sys
from io import StringIO


class MyTestCase(unittest.TestCase):
    def test_viewModel(self):
        strio = StringIO(u"-User;author[y,l15,w36,a1]:i;bg[t,l,r,b]:i;title(f14,cw);id[x,y](ch):l;url(cwa):b;mobile:f;bgView(cwa):v")
        sys.stdin = strio
        bxuimodel.main()

    def test_viewController(self):
        strio = StringIO(u"-User(m=ProductItem,req,adapter):vc;author[y,l15,w36,a1]:i;bg[t,l,r,b]:i;title(f14,cw);id[x,y](ch):l;url(cwa):b;mobile:f;bgView(cwa):v")
        sys.stdin = strio
        bxuimodel.main()


if __name__ == '__main__':
    unittest.main()
