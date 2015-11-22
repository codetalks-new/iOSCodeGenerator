#-*- coding:utf-8 -*-

import unittest
import os
import sys
sys.path.insert(0, os.path.basename('..'))

from io import StringIO
from ios_code_generator import bxoutlet

class MyTestCase(unittest.TestCase):
    def test_outlet(self):
        strio = StringIO(u"label:l;name(required):f;button:b;view:v;imageView:i;field:f;addr:tc")
        sys.stdin = strio
        bxoutlet.main()


if __name__ == '__main__':
    unittest.main()
