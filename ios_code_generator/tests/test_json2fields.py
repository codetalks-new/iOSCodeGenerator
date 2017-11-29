# -*- coding: utf-8 -*-
from StringIO import StringIO

import sys

from ios_code_generator import utils
from ios_code_generator.generators import json_to_fields, json_escape_quote, json_remove_comment

__author__ = 'banxi'

def test_json2fields():
    strio = StringIO(u"""
"no": "qc1",
"category": "汽 ",
"name": "兰博基尼  ",
"price": 7388800,
"stock": 1,
"tp": 8127680,
"level": 100,
"picture": ""
    """)
    sys.stdin = strio
    json_to_fields()

def test_json2fields2():
    strio = StringIO(u"""
{
    "id" : 409727,
    "title" : "为什么 Linux 得 shell 不直接使用 JavaScript 的语法",
    "url" : "http://www.v2ex.com/t/409727",
    "content" : "另起炉灶有意思吗",
    "content_rendered" : "x",
    "replies" : 108,
    "member" : {
        "id" : 254032,
        "username" : "86322989",
        "tagline" : "",
        "avatar_mini" : "//v2ex.assets.uxengine.net/avatar/838b/31da/254032_mini.png?m=1507543878",
        "avatar_normal" : "//v2ex.assets.uxengine.net/avatar/838b/31da/254032_normal.png?m=1507543878",
        "avatar_large" : "//v2ex.assets.uxengine.net/avatar/838b/31da/254032_large.png?m=1507543878"
    },
    "node" : {
        "id" : 11,
        "name" : "linux",
        "title" : "Linux",
        "title_alternative" : "Linux",
        "url" : "http://www.v2ex.com/go/linux",
        "topics" : 3729,
        "avatar_mini" : "//v2ex.assets.uxengine.net/navatar/6512/bd43/11_mini.png?m=1511095631",
        "avatar_normal" : "//v2ex.assets.uxengine.net/navatar/6512/bd43/11_normal.png?m=1511095631",
        "avatar_large" : "//v2ex.assets.uxengine.net/navatar/6512/bd43/11_large.png?m=1511095631"
    },
    "created" : 1511704130,
    "last_modified" : 1511771913,
    "last_touched" : 1511773044
}
    """)
    sys.stdin = strio
    json_to_fields()

def test_json_remove_comments():
    text = u"""

    """

    in_lines = text.splitlines()
    lines = json_remove_comment(in_lines)
    ouput_text = "\n".join(lines)
    print(ouput_text)

def test_json_escape_quote():
    strio = StringIO(u"""

        """)
    sys.stdin = strio
    lines = utils.readlines_from_stdin()
    output_lines = json_escape_quote(lines)
    text = "".join(output_lines)
    print(text)

