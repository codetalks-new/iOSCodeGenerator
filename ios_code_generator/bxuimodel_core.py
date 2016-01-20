# -*- coding: utf-8 -*-
from __future__ import  unicode_literals
import sys
__author__ = 'banxi'

from .parser import  parse_source

def _readlines_from_stdin():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if isinstance(line, str):
            line = line.decode(encoding='utf-8')
        lines.append(line)
    return


def generate(target='uimodel', **options):
    print("// Build for target " + target)
    lines = _readlines_from_stdin()
    comments = ["//"+line for line in lines]
    model_decl,uifields = parse_source(lines)

    from .helper import jinja2_env
    template = jinja2_env.get_template('bx%s_tpl.html' % target)
    has_textfield = len([field for field in uifields if field.ftype == 'f']) > 0
    text = template.render(model=model_decl, uifields=uifields, has_textfield=has_textfield, comments=comments)
    return text.encode('utf-8')
