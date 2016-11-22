# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from StringIO import StringIO

import sys

from ios_code_generator.generators import generate_v2

__author__ = 'banxi'


def test_viewModel():
    strio = StringIO(
        u"-UserTableViewCell(m=User):tc\nauthor[y,l15,w36,a1](tint=ca):i;bg[e0]:i;title[bl8@author](f14,cw,text=我的);id[x,y](ch):l;url(cwa):b;mobile:f;bgView(cwa):v")
    sys.stdin = strio
    output = generate_v2("view")
    print(output)

def test_fontConfig():
    strio = StringIO(
        u"-UserTableViewCell(m=User):tc\ntitle(f14,cw,text=我的)")
    sys.stdin = strio
    output = generate_v2("view")
    print(output)

def test_goodsCell():
    strio = StringIO(u"""
    GoodsCell(m=Goods):tc
    icon[y, w64, a1, l15]:i
    title[t0@icon, at15@icon](f17, cpt)
    desc[bl4@title, l0@title](f13, cst)
    fee[t0@title, r15](cw, f15):il
    """)
    sys.stdin = strio
    output = generate_v2("view")
    print(output)

