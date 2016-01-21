# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import utils
from .parser import parse_source
from .helper import jinja2_env

__author__ = 'banxi'


def generate(target='uimodel', **options):
    print("// Build for target " + target)
    lines = utils.readlines_from_stdin()
    comments = ["//"+line for line in lines]
    model_decl,uifields = parse_source(lines)

    template = jinja2_env.get_template('bx%s_tpl.html' % target)
    has_textfield = len([field for field in uifields if field.ftype == 'f']) > 0
    text = template.render(model=model_decl, uifields=uifields, has_textfield=has_textfield, comments=comments)
    return text.encode('utf-8')