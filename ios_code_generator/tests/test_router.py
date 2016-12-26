#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import sys
from StringIO import StringIO
from ios_code_generator.generators import generate

def test_bxrouter1():
    strio = StringIO(u"""
-ApiRouter(prefix=api/appShop)
/api/appShop/registerPush?deviceToken=
/api/appShop/index
    """)
    sys.stdin = strio
    output = generate('router')
    print(output)

def test_bxrouter_01():
    strio = StringIO( u'''
    -CommonApiRouter(prefix=v1)\n
    /v1/signup(params,c=注册):post
    /v1/login(params,c=登录):post
    /v1/token/refresh/(params,c=更新Token):patch
    v1/logout/?login_id(c=注销登录):delete
    '''
    )
    sys.stdin = strio
    output = generate('router')
    print(output)

def test_no_model():
    strio = StringIO(u'''
    /v1/signup(params,c=注册):post
    /v1/login(params,c=登录):post
    /v1/token/refresh/(params,c=更新Token):patch
    v1/logout/?login_id(c=注销登录):delete
    '''
                     )
    sys.stdin = strio
    output = generate('router')
    print(output)

def test_api_service():
    strio = StringIO(u'''
    -ApiRouter(prefix=v1)\n
    /v1/signup(params,c=注册):post
    /v1/login(params,c=登录):post
    /v1/token/refresh/(params,c=更新Token):patch
    v1/logout/?login_id(c=注销登录):delete

    ''')
    sys.stdin = strio
    output = generate('api_service')
    print(output)
