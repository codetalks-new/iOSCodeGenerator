#-*- coding:utf-8 -*-
__author__ = 'banxi'

import unittest
from ios_code_generator import bxmodel
import sys
from io import StringIO

class MyTestCase(unittest.TestCase):
    def test_something(self):
        strio = StringIO(u"-User,id:i,url:u,title,author:r,counts:[i,created:di,realname\n")
        sys.stdin = strio
        bxmodel.main()


if __name__ == '__main__':
    unittest.main()
