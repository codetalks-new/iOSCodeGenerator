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

    def test_bxrouter_01(self):
        strio = StringIO( u'''
        -CommonApiRouter(prefix=v1)\n
        /v1/signup(params,c=注册):post
        /v1/login(params,c=登录):post
        /v1/token/refresh/(params,c=更新Token):patch
        v1/logout/?login_id(c=注销登录):delete
        '''
        )
        sys.stdin = strio
        bxrouter.main()

    def test_bxapiService(self):
        strio = StringIO(u'''
        -ApiRouter(prefix=v1)\n
        /v1/signup(params,c=注册):post
        /v1/login(params,c=登录):post
        /v1/token/refresh/(params,c=更新Token):patch
        v1/logout/?login_id(c=注销登录):delete

        ''')
        sys.stdin = strio
        bxrouter.main('api_service')


if __name__ == '__main__':
    unittest.main()
