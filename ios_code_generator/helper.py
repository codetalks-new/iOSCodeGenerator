# -*- coding: utf-8 -*-
__author__ = 'banxi'
from jinja2 import PackageLoader,Environment
jinja2_loader = PackageLoader('ios_code_generator', 'tpl')
jinja2_env = Environment(loader=jinja2_loader, trim_blocks=True, lstrip_blocks=True)