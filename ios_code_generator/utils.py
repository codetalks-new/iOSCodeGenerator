# -*- coding: utf-8 -*-
__author__ = 'banxi'


def snakelize_word(name):
    ''' userLike -> UserLike '''
    if not name:
        return name
    first_char = name[0].upper()
    return first_char+name[1:]

def snakelize(name):
    ''' user-like-add -> UserLikeAdd '''
    words = name.split("_")
    return ''.join([snakelize_word(word) for word in words if word])
