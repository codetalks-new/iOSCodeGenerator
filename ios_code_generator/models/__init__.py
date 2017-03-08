# -*- coding: utf-8 -*-

__author__ = 'banxi'

from .core import *

def _auto_import_models():
    import os
    import importlib
    searchpath = os.path.dirname(__file__)
    exclude_modules = ['__init__', 'core']
    for filename in os.listdir(searchpath):
        if not filename.endswith('.py'):
            continue
        module_name = filename[:-3]
        if module_name in exclude_modules:
            continue
        importlib.import_module("."+module_name, 'ios_code_generator.models')

# 由于 Model generator 使用装饰器自动注册的机制, 所以需要模块导入之后才能自动注册,所以在这里需要自动导入.
_auto_import_models()

