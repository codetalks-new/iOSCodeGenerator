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
-ApiRouter(prefix=api/appShop)
 /api/appShop/registerPush?deviceToken=
 /api/appShop/index
        """)
        sys.stdin = strio
        bxrouter.main()

    def test_bxrouter2(self):
        strio = StringIO( u' -JobApiRouter(prefix=appJob)\n /appJob/companyInfoUpdate(params,c=中文-结构):post')
        sys.stdin = strio
        bxrouter.main()

    def test_bxapiService(self):
        strio = StringIO(u'''
-ApiRouter(prefix=/api)
/api/user/sign_up(params):p
/api/user/sign_in(params):p
/api/user/forget_code(params):p
/api/user/forget_set(params):p
/api/user/my
/api/user/cash_list
/api/user/msg_list?page=1
/api/user/msg_detail?id=1
/api/user/profile(params):p
/api/user/feedback(params):p
/api/user/alipay_add(params):p
/api/user/bank_add(params):p
/api/industry/list(params)
/api/category/list(params)
/api/company/add(params):p
/api/device/add(params):p
/api/device/edit(params):p
/api/device/list?page=1
/api/device/detail?id=1

        ''')
        sys.stdin = strio
        bxrouter.main('api_service')


if __name__ == '__main__':
    unittest.main()
