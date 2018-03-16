#-*- coding:utf-8 -*-
import unittest
import sys
import os
from io import StringIO
from ios_code_generator.generators import generate

__author__ = 'banxi'

def test_data_model():
    strio = StringIO(u"-User(tos,hash,eq,ctor)\nid:i;url:[u;title;author:r;follows(type=Follow):[r;counts:[i;created:di;realname\n")
    sys.stdin = strio
    text = generate("model")
    print(text)

def test_refModel():
    strio = StringIO(u"-ShopCard\nshopCardBase:r;shopCardLog(field=logs):[r\n")
    sys.stdin = strio
    text = generate("model")
    print(text)

def test_with_underscore():
    strio = StringIO(u"""
PlayerInfo
userid;nickname;avatar:u;buyin:i;income:i;permission:i
    """)
    sys.stdin = strio
    text = generate("model")
    print(text)

def test_json2fields():
    strio = StringIO(u''' "id":"20", "name":"\u4e1c\u76df\u7ecf\u6d4e\u5f00\u53d1\u533a", "distrct":[ ] ''')
    sys.stdin = strio



