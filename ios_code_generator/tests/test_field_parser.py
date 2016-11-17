# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.models import DataModel
from ios_code_generator.models import Model

__author__ = 'banxi'

def test_parse_field_info():
    field1 = Model.parse_field_info("title:s")
    assert field1
    assert field1.name == 'title'
    assert field1.ftype == 's'

def test_parse_model_field_info():
    field1 = DataModel.parse_field_info("title:s")
    assert field1.name == 'title'
    assert field1.ftype == 's'
    assert field1.type_class == 'String'

    field2 = DataModel.parse_field_info('CardLog:[r')
    assert field2
    assert field2.name == "CardLog"
    assert field2.ftype == "[r"
    assert field2.type_class == 'CardLog'
    assert field2.field_name == 'cardLog'

    field3 = DataModel.parse_field_info('CardLog:r')
    assert field3
    assert field3.name == "CardLog"
    assert field3.ftype == "r"
    assert field3.type_class == 'CardLog'
    assert field3.field_name == 'cardLog'
