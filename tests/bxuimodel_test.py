import unittest

import bxuimodel
import sys
from io import StringIO


class MyTestCase(unittest.TestCase):
    def test_something(self):
        strio = StringIO(u"-User;author[y,l15,w36,a1]:i;title;id[x,y]:l;url:b;mobile:f")
        sys.stdin = strio
        bxuimodel.main()


if __name__ == '__main__':
    unittest.main()
