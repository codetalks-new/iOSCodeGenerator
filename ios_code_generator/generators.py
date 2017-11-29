# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import functools

import sys

from . import utils
from .helper import jinja2_env

__author__ = 'banxi'

_generators_map = {}


def _make_gkey(target, platform, lang):
    return "%s:%s:%s" % (target, platform, lang)

def as_generator(target, platform="ios", lang="swift"):
    def decorator(cls):
        gkey = _make_gkey(target=target, platform=platform, lang=lang)
        cls.target = target
        cls.platform = platform
        cls.lang = lang
        _generators_map[gkey] = cls
        return cls
    return decorator

as_ios_swift_generator = functools.partial(as_generator, platform="ios", lang="swift")
as_android_kotlin_generator = functools.partial(as_generator, platform="android", lang="kotlin")

def find_generator(target, platform="ios", lang="swift"):
    gkey = _make_gkey(target=target, platform=platform, lang=lang)
    return _generators_map.get(gkey)



def generate_v2(target, **options):
    from . import models
    platform = options.get('platform', 'ios')
    lang = options.get('lang', 'swift')
    lines = utils.readlines_from_stdin()
    comments = ["//"+line for line in lines]

    model_class = find_generator(target=target, platform=platform, lang=lang)
    if not model_class:
        return "No generator for %s %s %s" % (target, platform, lang)
    try:
        model,fields = model_class.parse_source(lines)
        template_path = model.template_path()
        template_context = model.template_context()
        template_context['comments'] = comments
        template = jinja2_env.get_template(template_path)
        text = template.render(**template_context)
        return text.encode('utf-8')
    except Exception as e:
        import traceback
        return traceback.format_exc()

generate = generate_v2

generate_kotlin = functools.partial(generate_v2, platform='android', lang='kotlin')

def json_to_fields(auto_remove_comments = False):
    from . import converters
    try:
        lines = utils.readlines_from_stdin()
        comments = [str("\n/// ") + line.encode('utf-8') for line in lines]
        if auto_remove_comments:
            final_lines = json_remove_comment(lines)
        else:
            final_lines = lines
        text = '\n'.join(final_lines)
        fields = converters.convert_text_to_field_list(text)
        output = ';'.join([str(f) for f in fields])
        sys.stdout.writelines(comments)
        sys.stdout.write("\n"+output)
    except Exception as e:
        import traceback
        sys.stdout.write(traceback.format_exc())

def json_remove_comment(lines):
    # remove '//' comment in lines
    final_lines = []
    for line in lines:
        if not line:
            continue
        comment_index = line.rfind('//')
        if comment_index == 0:
            continue  # comment line
        if comment_index == -1:
            comment_index = line.rfind('#')
        if comment_index == 0:
            continue  # comment line

        if comment_index > 0:
            new_line = line[:comment_index]
            final_lines.append(new_line)
        else:
            final_lines.append(line)
    return final_lines

def json_escape_quote(lines = None):
    should_return = lines is not None
    lines = lines or utils.readlines_from_stdin()
    in_lines = json_remove_comment(lines)
    final_lines = []
    for line in in_lines:
        if not line:continue
        new_line = line.replace('"','\\"')
        final_lines.append(new_line)
    if should_return:
        return  final_lines
    else:
        ouput_lines =([line.decode('utf-8') for line in final_lines])
        ouput_lines.insert(0, '"')
        ouput_lines.append('"')
        sys.stdout.writelines(ouput_lines)
