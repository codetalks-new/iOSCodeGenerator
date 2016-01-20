# -*- coding: utf-8 -*-
from __future__ import  unicode_literals
__author__ = 'banxi'

import re


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
    words = re.split('[_-]', field_name)
    return ''.join([camelize_word(word) for word in words if word])