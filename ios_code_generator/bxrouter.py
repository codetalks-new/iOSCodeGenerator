# -*- coding: utf-8 -*-
from __future__ import  unicode_literals
__author__ = 'banxi'
import sys
import re
import urlparse
from cached_property import cached_property
from . import utils
from . import parser
from .helper import jinja2_env

FIELD_DELIMETER = ';'


# User(/)

# api/product/isuser_product?id=24351


class Router(object):
    def __init__(self,model, req, method='get', attrs=None):
        super(Router, self).__init__()
        self.model = model
        self.req = req
        self.method = method
        self.attrs = attrs if attrs else {}
        parse_result = urlparse.urlparse(req)
        self.query_dict = urlparse.parse_qs(parse_result.query, keep_blank_values=True)
        self.raw_path_comps = [p for p in parse_result.path.split('/') if p]

    @cached_property
    def is_public(self):
        return 'p' in self.attrs

    @cached_property
    def is_post(self):
        return self.method in ['p','post']

    def treat_last_id_path_as_query(self):
        if self.model:
            return self.model.has_attr('idpath',True)
        else:
            return True

    @property
    def comment(self):
        return self.attrs.get('c', '')

    @cached_property
    def path_comps(self):
        path_comps = self.raw_path_comps
        if len(path_comps) > 2:
            if "id" in path_comps[-2] and path_comps[-1].isdigit():
                self.query_dict[path_comps[-2]] = path_comps[-1]
                path_comps = path_comps[:-2]
        return path_comps

    @cached_property
    def path(self):
        return '/'.join(self.path_comps)

    @cached_property
    def ignored_name_prefix(self):
        prefix = self.model.prefix if self.model else 'api'
        if prefix:
            return prefix
        else:
            return 'api'

    @cached_property
    def name(self):
        prefix = self.ignored_name_prefix
        path_comps = self.path_comps
        if path_comps[0] == prefix:
            path_comps = path_comps[1:]
        return ''.join([utils.snakelize(comp) for comp in path_comps if comp])

    @cached_property
    def dot_name(self):
        if self.has_param:
            return ".%s(_)" % self.name
        else:
            return ".%s" % self.name

    @cached_property
    def has_param(self):
        if self.has_params:
            return True
        return bool(self.query_dict)

    @cached_property
    def has_params(self):
        return 'params' in self.attrs

    @cached_property
    def only_one_param(self):
        if self.has_params:
            return False
        return len(self.query_dict) == 1

    @cached_property
    def first_query_name(self):
        return self.query_dict.keys()[0]

    @property
    def case_stmt(self):
        if self.has_param:
            if self.only_one_param:
                return 'case %s(%s:String)' % (self.name, self.first_query_name)
            else:
                return 'case %s(params:Params)' % self.name
        else:
            return 'case %s' % self.name

    @property
    def path_stmt(self):
        if self.has_param:
            return 'case .%s(_): return "%s"' % (self.name, self.path)
        else:
            return 'case .%s: return "%s"' % (self.name, self.path)

    @property
    def params_stmt(self):
        if not self.has_param:
            return ''
        if self.only_one_param:
            return 'case .{name}(let {key}):return ["{key}":{key}]'.format(name=self.name, key=self.first_query_name)
        else:
            return 'case .%s(let params): return params' % self.name

router_pattern = re.compile(r'(?P<req>[^,;\(\)]+)(?:\((?P<attrs>[\w=,-/\u4e00-\u9fcc]+)\))?')
model_pattern = re.compile(r'(?P<name>\w+)(?:\((?P<attrs>[\w=,/\u4e00-\u9fcc]+)\))?')

def parse_route(info, model=None):
    parts = re.split(':', info.strip())
    req_info = parts[0]
    method = parts[1] if len(parts) > 1 else 'get'
    matcher = router_pattern.match(req_info)
    groupdict = matcher.groupdict()
    req = groupdict.get('req')
    attrs_str = groupdict.get('attrs')
    attr_list = parser.parse_field_config(attrs_str)
    attrs = dict( [(item.ctype,item) for item in attr_list] )
    return Router(model,req,method,attrs)


def parse_source(lines):
    model = None
    if lines[0].startswith('-'):
       model =  parser.parse_model(lines[0])
       lines = lines[1:]
    routers = []
    for line in lines:
        router = parse_route(line,model=model)
        routers.append(router)
    return model,routers


def main(**options):
    target = "router"
    print("// Build for router ")
    lines = utils.readlines_from_stdin()
    model,router_list = parse_source(lines)
    comments = ["//"+line for line in lines]
    template = jinja2_env.get_template('bx%s_tpl.html' % target)
    public_routers = [r for r in router_list if r.is_public]
    post_routers = [r for r in router_list if r.is_post]
    text = template.render(model=model,comments=comments, routers=router_list, public_routers=public_routers, post_routers=post_routers)
    print(text.encode('utf-8'))
