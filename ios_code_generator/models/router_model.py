# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import urlparse

import itertools

from ios_code_generator.generators import as_ios_swift_generator
from ios_code_generator.models import Model, Field
from ios_code_generator.utils import cached_property, to_camel_case, to_mixed_case

__author__ = 'banxi'

_method_map = {
    'p':'post',
    'g': 'get',
    'd': 'delete'
}

class RouterField(Field):
    def __init__(self, req, method, attrs, model):
        self.model = model
        self.req = req
        self.method = method
        self.attrs = attrs if attrs else {}
        parse_result = urlparse.urlparse(req)
        self.query_dict = urlparse.parse_qs(parse_result.query, keep_blank_values=True)
        self.raw_path_comps = [p for p in parse_result.path.split('/') if p]
        name = self.calc_name()
        super(RouterField, self).__init__(name, method, attrs)

    @cached_property
    def ignored_name_prefix(self):
        prefix = self.model.prefix if hasattr(self, 'model') else 'api'
        if prefix:
            return prefix
        else:
            return 'api'

    @cached_property
    def prefix_comps(self):
        return self.ignored_name_prefix.split('/')

    @cached_property
    def path_comps(self):
        path_comps = self.raw_path_comps
        if len(path_comps) > 2:
            if "id" in path_comps[-2] and path_comps[-1].isdigit():
                self.query_dict[path_comps[-2]] = path_comps[-1]
                path_comps = path_comps[:-2]
        return path_comps

    def calc_name(self):
        prefixs = self.prefix_comps
        path_comps = self.path_comps
        for p in prefixs:
            if path_comps[0] == p:
                path_comps = path_comps[1:]
        step1_name = ' '.join([comp for comp in path_comps if comp])
        return to_mixed_case(step1_name)

    @cached_property
    def is_public(self):
        return 'p' in self.attrs

    @cached_property
    def is_post(self):
        return self.method in ['p', 'post']

    @cached_property
    def method_name(self):
        name = _method_map.get(self.method)
        if name:
            return name
        else:
            return self.method.lower()

    def treat_last_id_path_as_query(self):
        if self.model:
            return self.model.has_attr('idpath', True)
        else:
            return True

    @property
    def comment(self):
        return self.attrs.get('c', '')

    @cached_property
    def group_name(self):
        if 'group' in self.attrs:
            return self.attrs.get('group').config_value
        return 'api'



    @cached_property
    def path(self):
        return '/'.join(self.path_comps)


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



@as_ios_swift_generator("router")
class RouterModel(Model):
    field_class =  RouterField

    @classmethod
    def parse_route(cls, info, model):
        parts = re.split(':', info.strip())
        req_info = parts[0]
        method = parts[1] if len(parts) > 1 else 'get'
        matcher = router_pattern.match(req_info)
        groupdict = matcher.groupdict()
        req = groupdict.get('req')
        attrs_str = groupdict.get('attrs')
        attr_list = cls.parse_field_config(attrs_str)
        attrs = {item.ctype: item for item in attr_list }
        return RouterField(req, method, attrs, model)


    @classmethod
    def parse_source(cls, lines):
        if lines[0].startswith('-'):
            model = cls.parse_model_line(lines[0])
            lines = lines[1:]
        else:
            model = cls(name=cls.FRAGMENT_NAME)
        routers = []
        for line in lines:
            router = cls.parse_route(line, model)
            routers.append(router)
        model.fields = routers
        return model, routers

    @property
    def routers(self):
        return self.fields

    def template_context(self):
        ctx = super(RouterModel, self).template_context()
        public_routers =  [r for r in self.routers if r.is_public]
        post_routers = [r for r in self.routers if r.is_post]
        ctx.update(routers=self.routers,public_routers=public_routers, post_routers=post_routers)
        return ctx


class GroupRouters(object):
    def __init__(self,name,routers):
        self.name = name
        self.routers = routers

    @cached_property
    def service_name(self):
        return to_camel_case(self.name + 'Service')

def group_routers(routers):
    gr_list = []
    for k,g in itertools.groupby(routers,key=lambda x:x.group_name):
        gr = GroupRouters(k,routers=list(g))
        gr_list.append(gr)
    return gr_list

@as_ios_swift_generator("api_service")
class ApiServiceModel(RouterModel):

    def template_context(self):
        ctx = super(ApiServiceModel, self).template_context()
        groups = group_routers(self.routers)
        ctx['groups'] = groups
        return ctx


