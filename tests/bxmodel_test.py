#-*- coding:utf-8 -*-
__author__ = 'banxi'

import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, os.path.basename('..'))
from ios_code_generator import bxmodel

class MyTestCase(unittest.TestCase):
    def test_something(self):
        strio = StringIO(u"-User,id:i,url:u,title,author:r,follow:[r,counts:[i,created:di,realname\n")
        sys.stdin = strio
        bxmodel.main()

    def test_refModel(self):
        strio = StringIO(u"-ShopCard,ShopCardBase:r,ShopCardLog:[r\n")
        sys.stdin = strio
        bxmodel.main()

    def test_json2fields(self):
        strio = StringIO(u''' "id":"20", "name":"\u4e1c\u76df\u7ecf\u6d4e\u5f00\u53d1\u533a", "distrct":[ ] ''')
        sys.stdin = strio
        bxmodel.json_to_fields()



if __name__ == '__main__':
    unittest.main()
