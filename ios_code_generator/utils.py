# -*- coding: utf-8 -*-
from __future__ import  unicode_literals
__author__ = 'banxi'

import re
import sys

def snakelize_word(name):
    ''' userLike -> UserLike '''
    if not name:
        return name
    first_char = name[0].upper()
    return first_char+name[1:]

def snakelize(name):
    ''' user-like-add -> UserLikeAdd '''
    words = re.split('[_-]', name)
    return ''.join([snakelize_word(word) for word in words if word])

def camelize_word(word):
    return word[0].lower() + word[1:]


def camelize(field_name):
    name = snakelize(field_name)
    return camelize_word(name)

def readlines_from_stdin():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if isinstance(line, str):
            line = line.decode(encoding='utf-8')
        lines.append(line)
    return lines