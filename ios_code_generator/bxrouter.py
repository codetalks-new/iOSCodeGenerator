# -*- coding: utf-8 -*-
__author__ = 'banxi'
import sys
import re
import urlparse

FIELD_DELIMETER = ';'


# User(/)

# api/product/isuser_product?id=24351

def _to_snake_case(name):
    words = name.split("_")
    return ''.join([word.capitalize() for word in words if word])


class Router(object):
    def __init__(self, req, is_public=False, is_post=False):
        super(Router, self).__init__()
        self.is_public = is_public
        self.is_post = is_post
        parse_result = urlparse.urlparse(req)
        self.query_dict = urlparse.parse_qs(parse_result.query, keep_blank_values=True)
        path_comps = [p for p in parse_result.path.split('/') if p]
        self.path_comps = path_comps
        if len(path_comps) > 2:
            if "id" in path_comps[-2] and path_comps[-1].isdigit():
                self.query_dict[path_comps[-2]] = path_comps[-1]
                path_comps = path_comps[:-2]

        self.path = '/'.join(path_comps)

        if path_comps[0] == 'api':
            path_comps = path_comps[1:]

        self.name = ''.join([_to_snake_case(comp) for comp in path_comps if comp])

    @property
    def dot_name(self):
        if self.has_param:
            return ".%s(_)" % self.name
        else:
            return ".%s" % self.name

    @property
    def has_param(self):
        return bool(self.query_dict)

    @property
    def only_one_param(self):
        return len(self.query_dict) == 1

    @property
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

router_pattern = re.compile(r'(?P<req>[^,;\(\)]+)(?:\((?P<attrs>[\w=,]+)\))?')
model_pattern = re.compile(r'(?P<name>\w+)(?:\((?P<attrs>[\w=,]+)\))?')

def parse_route_info(info):
    parts = re.split(':', info.strip())
    req_info = parts[0]
    is_post = 'p' in parts[1] if len(parts) > 1 else False
    matcher = router_pattern.match(req_info)
    groupdict = matcher.groupdict()
    req = groupdict.get('req')
    attrs = groupdict.get('attrs')
    is_public = 'p' in attrs if attrs else False
    return Router(req, is_public=is_public, is_post=is_post)


def parse_line(line):
    infos = line.split(FIELD_DELIMETER)
    routers = []
    for info in infos:
        info = info.strip()
        if info:
            router = parse_route_info(info)
            routers.append(router)
    return routers


def main(**options):
    target = "router"
    print("// Build for router ")
    router_list = []
    comments = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            if isinstance(line, str):
                line = line.decode(encoding='utf-8')
            comments.append("// " + line)
            routers = parse_line(line)
            if routers:
                router_list.extend(routers)
    from .helper import jinja2_env
    template = jinja2_env.get_template('bx%s_tpl.html' % target)
    public_routers = [r for r in router_list if r.is_public]
    post_routers = [r for r in router_list if r.is_post]
    text = template.render(comments=comments, routers=router_list, public_routers=public_routers, post_routers=post_routers)
    print(text.encode('utf-8'))
