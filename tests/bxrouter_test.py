#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import unittest

import os
import sys
sys.path.insert(0, os.path.basename('..'))

from ios_code_generator import bxrouter
from StringIO import StringIO


class MyTestCase(unittest.TestCase):
    def test_bxrouter(self):
        strio = StringIO(u"""
        -BXRouter
        api/product/isuser_product?id=24351:p
        api/product/addUserProduct?id=24351
        api/explore/explore_list?categoryId=&page=&size=10&exploreType=&title=
        api/baike?id=101(p)
        api/discover/commect_updo/id/47:p
        """)
        sys.stdin = strio
        bxrouter.main()

    def test_bxrouter2(self):
        strio = StringIO( u' -JobApiRouter(prefix=appJob)\n /appJob/companyInfoUpdate(params,c=中文-结构):post')
        sys.stdin = strio
        bxrouter.main()


if __name__ == '__main__':
    unittest.main()
