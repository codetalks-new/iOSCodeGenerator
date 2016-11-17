# -*- coding: utf-8 -*-
from __future__ import  unicode_literals
__author__ = 'banxi'

import re
import sys

# mixedCase
# CamelCase
# snake_case

_name_comps_delimiter_re = re.compile("[\s_-]")


def lower_first_char(word):
    if not word:
        return word
    return word[0].lower() + word[1:]


def upper_first_char(word):
    if not word:
        return word
    return word[0].upper() + word[1:]


def to_mixed_case(name):
    return lower_first_char(to_camel_case(name))


def to_camel_case(name):
    if not name:
        return name

    words = _name_comps_delimiter_re.split(name)
    parts = [upper_first_char(word) for word in words]
    return ''.join(parts)


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


## taken from werkzeug

class _Missing(object):

    def __repr__(self):
        return 'no value'

    def __reduce__(self):
        return '_missing'

_missing = _Missing()


class cached_property(property):

    """A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value::

        class Foo(object):

            @cached_property
            def foo(self):
                # calculate something important here
                return 42

    The class has to have a `__dict__` in order for this property to
    work.
    """

    # implementation detail: A subclass of python's builtin property
    # decorator, we override __get__ to check for a cached value. If one
    # choses to invoke __get__ by hand the property will still work as
    # expected because the lookup logic is replicated in __get__ for
    # manual invocation.

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = value

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value

