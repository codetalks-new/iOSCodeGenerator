# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.android_constraint_generator import find_generator_by_config
from ios_code_generator.enviroment import ConstraintConfigItem

__author__ = 'banxi'

def test_leading():
    config1 = ConstraintConfigItem(ctype='l')
    stmts1 = find_generator_by_config(config1).generate_stmts()
    assert len(stmts1) == 1
    assert  'app:layout_constraintLeft_toLeftOf="parent"' in  stmts1

    config2 = ConstraintConfigItem(ctype='l', value='8')
    stmts2 = find_generator_by_config(config2).generate_stmts()
    assert len(stmts2) == 2
    assert  'app:layout_constraintLeft_toLeftOf="parent"' in  stmts2
    assert  'android:layout_marginStart="8dp"' in  stmts2

    config3 = ConstraintConfigItem(ctype='l', secondItem='name')
    stmts3 = find_generator_by_config(config3).generate_stmts()
    assert len(stmts3) == 1
    assert  'app:layout_constraintLeft_toLeftOf="name"' in  stmts3

def test_size():
    wcfg =  ConstraintConfigItem(ctype='w', value='100')
    wstmts = find_generator_by_config(wcfg).generate_stmts()
    assert len(wstmts) == 1
    assert 'android:layout_width="100dp"' in wstmts

    hcfg =  ConstraintConfigItem(ctype='h', value='100')
    hstmts = find_generator_by_config(hcfg).generate_stmts()
    assert len(hstmts) == 1
    assert 'android:layout_height="100dp"' in hstmts