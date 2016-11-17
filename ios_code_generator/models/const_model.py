# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_ios_swift_generator
from ios_code_generator.models import Field
from ios_code_generator.models import Model

__author__ = 'banxi'


@as_ios_swift_generator("const")
class ConstModel(Model):
    field_class = Field