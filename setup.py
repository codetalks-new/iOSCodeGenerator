# -*- coding: utf-8 -*-
__author__ = 'banxi'
from setuptools import setup

setup(
    name='ios_code_generator',
    version='0.2.0',
    author='Haizhen Lee',
    author_email='banxi1988@gmail.com',
    install_requires = ['jinja2'],
    description='iOS Code Generator',
    packages=['ios_code_generator'],
    package_data={'ios_code_generator': ['tpl/*.html']},
    license='MIT'
)
