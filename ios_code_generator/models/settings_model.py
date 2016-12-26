# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_ios_swift_generator
from ios_code_generator.maps import settings_raw_type_map
from ios_code_generator.models import Model, Field
from ios_code_generator.models import model_property

__author__ = 'banxi'

class SettingsField(Field):

    @property
    def settings_name(self):
        return self.name

    @property
    def settings_key(self):
        prefix = self.model.prefix
        if prefix:
            return "%s_%s" % (prefix, self.name)
        else:
            return self.name

    @property
    def settings_type(self):
        return settings_raw_type_map.get(self.ftype, 'String')

    @property
    def settings_default_value(self):
        map = {
            'i': '0',
            'b': 'false',
            'f': '0',
            's': '""',
            '':'""'
        }
        return map.get(self.ftype, 'nil')

    @property
    def settings_type_annotation(self):
        t = self.settings_type
        if self.ftype in ['b','i','f']:
            return t
        else:
            return t+"?"

    @property
    def settings_getter_type(self):
        map = {
            'i':'integer',
            'b':'bool',
            'f':'double',
            'u':'URL',
            's':'string',
            'd': 'object'
        }
        return map.get(self.ftype,'string')

    @property
    def settings_set_stmt(self):
        key = 'Keys.%s' % self.settings_name
        return 'userDefaults.set(newValue,forKey:%s)' % (key)

    @property
    def settings_get_stmt(self):
        type = self.settings_getter_type
        key = 'Keys.%s' % self.settings_name
        stmt = 'return userDefaults.%s(forKey: %s)' % (type,key)
        if self.ftype == 'd':
            stmt += " as? Date"
        return stmt


@as_ios_swift_generator("settings")
class SettingsModel(Model):
    field_class = SettingsField

    @property
    def settings_prefix(self):
        return self.prefix

    @property
    def settings_sync_on_save(self):
        value = self.model_config.get('sync_on_save', 'true').lower()
        if value in ['1', 't', 'true', 'on']:
            return True
        return False

    @classmethod
    def parse_source(cls, lines):
        if lines[0].startswith('-'):
            model = cls.parse_model_line(lines[0])
            lines = lines[1:]
        else:
            model = cls(name=cls.FRAGMENT_NAME)
        model.fields = cls.parse_field_lines(lines)
        return model, model.fields
