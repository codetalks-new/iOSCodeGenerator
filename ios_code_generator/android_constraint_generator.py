# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'banxi'

ui_field_constraint_map = {
    'x': '',
    'y': '',
    'l': 'app:layout_constraintLeft_toLeftOf',
    't': 'app:layout_constraintTop_toTopOf',
    'r': 'app:layout_constraintRight_toRightOf',
    'b': 'app:layout_constraintBottom_toBottomOf',
    'w': 'android:layout_width',
    'h': 'android:layout_height',
    'a': 'pac_aspectRatio',
    'e': 'pac_edge',
    'hor': 'pac_horizontal',
    'ver': 'pac_vertical',
    'bl': 'app:layout_constraintTop_toBottomOf',
    'ab': 'app:layout_constraintBottom_toTopOf',
    'bf': 'app:layout_constraintRight_toLeftOf',
    'at': 'app:layout_constraintLeft_toRightOf',
}

ui_field_offset_map = {
    'x':' android:layout_marginStart',
    'y':' android:layout_marginTop',
    'l':' android:layout_marginStart',
    't':' android:layout_marginTop',
    'r':' android:layout_marginEnd',
    'b':' android:layout_marginBottom',
    'ab':' android:layout_marginBottom',
    'bf':' android:layout_marginEnd',
    'at':' android:layout_marginStart',
    'bl':' android:layout_marginTop',
}

name_field_map = dict()


def field_by_name(name):
    return name_field_map.get(name)


class _ConstraintGenerator(object):


    def __init__(self,config):
        self.config = config

    @property
    def anchor_name(self):
        anchor_name = self.config.secondItem
        if anchor_name:
            field = field_by_name(anchor_name)
            if field:
                return '@+id/%s' % field.id_name
            else:
                return '@+id/%s' % anchor_name

        return 'parent'

    @property
    def config_value(self):
        return self.config.value

    def generate_stmts(self):
        """返回生成的 约束语句
        """
        stmts = self.position_stmts()
        offset_stmt = self.offset_stmt()
        if offset_stmt:
            stmts.append(offset_stmt.strip())
        return stmts

    def position_stmts(self):
        constraint_attr_name = ui_field_constraint_map.get(self.config.ctype, '')
        stmt ='%s="%s"' %  (constraint_attr_name,self.anchor_name)
        return [stmt.strip()]

    def offset_stmt(self):
        value = self.config_value
        offset_type = ui_field_offset_map.get(self.config_value)
        if value and offset_type:
            stmt =  '%s="%sdp"' % (offset_type,value)
            return stmt.strip()


_constraint_type_generator_cls_map = dict()

def find_generator_by_config(config):
    cls = _constraint_type_generator_cls_map.get(config.ctype)
    if cls:
        return cls(config=config)
    return _ConstraintGenerator(config=config)

def register_as_constraint_generator(type):
    def decorator(cls):
        _constraint_type_generator_cls_map[type] = cls
        return cls
    return decorator



@register_as_constraint_generator('x')
class CenterXConstraint(_ConstraintGenerator):
    def position_stmts(self):
        stmts = []
        stmt = 'app:layout_constraintLeft_toLeftOf="%s"' %  self.anchor_name
        stmts.append(stmt.strip())
        stmt = 'app:layout_constraintRight_toRightOf="%s"' %  self.anchor_name
        stmts.append(stmt.strip())
        return stmts


@register_as_constraint_generator('y')
class CenterYConstraint(_ConstraintGenerator):
    def position_stmts(self):
        stmts = []
        stmt = 'app:layout_constraintTop_toTopOf="%s"' %  self.anchor_name
        stmts.append(stmt.strip())
        stmt = 'app:layout_constraintBottom_toBottomOf="%s"' %  self.anchor_name
        stmts.append(stmt.strip())
        return stmts


@register_as_constraint_generator('w')
@register_as_constraint_generator('h')
class SizeConstraint(_ConstraintGenerator):
    def generate_stmts(self):
        value = self.config_value or '0'
        size_attr_name = ui_field_constraint_map.get(self.config.ctype, '')
        stmt = '%s="%sdp"' % (size_attr_name,value)
        return [stmt.strip()]

