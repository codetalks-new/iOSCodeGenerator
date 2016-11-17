# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_ios_swift_generator
from ios_code_generator.maps import db_type_map
from ios_code_generator.models import Model, Field
from ios_code_generator.utils import cached_property

__author__ = 'banxi'

class DaoField(Field):

    @property
    def db_column_name(self):
        return db_type_map.get(self.ftype,'String')

@as_ios_swift_generator("dao")
class DaoModel(Model):
    field_class =  DaoField

    @cached_property
    def db_table_name(self):
        prefix = self.model_config.get('prefix','')
        if prefix:
            return "%s_%s" % (prefix,self.camel_name)
        else:
            return self.camel_name







