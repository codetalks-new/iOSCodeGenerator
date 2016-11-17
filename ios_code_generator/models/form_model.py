# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_ios_swift_generator
from ios_code_generator.models import model_bool_property
from ios_code_generator.models.view_model import ViewField, ViewModel

__author__ = 'banxi'

class FormField(ViewField):
    pass

@as_ios_swift_generator("form")
class FormModel(ViewModel):
    field_class = FormField
    has_keyboard = model_bool_property(['kb', 'keyboard'])