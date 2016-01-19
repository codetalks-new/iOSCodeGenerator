# -*- coding: utf-8 -*-
__author__ = 'banxi'
import sys
import re
from string import Template


char_type_map = {
    's': 'String',
    'i': 'Int',
    'f': 'Double',
    'd': 'Double',
    'b': 'Bool',
    'u': 'NSURL',
    'r': 'Ref',
    'j': 'JSON',
    'di': 'NSDate',
    'ds': 'NSDate',
    '[s': 'Array',
    '[i': 'Array',
    '[f': 'Array',
    '[d': 'Array',
    '[b': 'Array',
    '[r': 'RefArray'
}


def _field_name_to_type_name(field_name):
    words = re.split('_', field_name)
    if len(words) == 1 and field_name[0].isupper():
        return field_name
    return ''.join([word.capitalize() for word in words if word])

def _format_ref_field_name(field_name):
    if field_name[0].isupper():
        return field_name[0].lower() + field_name[1:]
    return field_name

def parse_field_info(field_info):
    parts = re.split(':', field_info.strip())
    fname = parts[0]
    fname = fname.replace('-', '_').replace('"', '')
    ftype = None
    if len(parts) > 1:
        ftype = parts[1]
    if not ftype:
        ftype = 's'
    type_class = char_type_map.get(ftype, 'String')
    declare = '    let {fname}:{type_class} '.format(fname=fname, type_class=type_class)
    dict_stmt = '   dict["{fname}"] = self.{fname}'.format(fname=fname)
    stmt = None
    if len(ftype) == 1:
        if ftype == 'r':
            type_name = _field_name_to_type_name(fname)
            fname = _format_ref_field_name(fname)
            declare = '    let {fname}:{type_class} '.format(fname=fname, type_class=type_name)
            stmt = ' self.{fname} = {type_name}(json:json["{fname}"])'.format(fname=fname, type_name=type_name)
            dict_stmt = 'dict["{fname}"] = self.{fname}.toDict()'.format(fname=fname)
        elif ftype == 'u':
            # NSURL
            stmt = '    self.{fname} = NSURL(string:json["{fname}"].stringValue)!'.format(fname=fname)
            dict_stmt = 'dict["{fname}"] = self.{fname}.absoluteString'.format(fname=fname)
        elif ftype == 'j':
            # JSON
            stmt = '    self.{fname} = json["{fname}"]'.format(fname=fname)
            dict_stmt = 'dict["{fname}"] = self.{fname}.object'.format(fname=fname)
        else:
            json_type = type_class.lower()
            stmt = '    self.{fname} = json["{fname}"].{json_type}Value'.format(fname=fname, json_type=json_type)
    elif len(ftype) == 2:
        type_complex = ftype[0]
        type_char = ftype[1]
        raw_type_class = char_type_map.get(type_char, 'String')
        if type_complex == '[':
            if type_char == 'r':
                type_name = _field_name_to_type_name(fname)
                fname = _format_ref_field_name(fname)
                declare = ' let {fname}:[{type_class}]'.format(fname=fname,type_class=type_name)
                stmt = '    self.{fname} = {type_class}.arrayFrom(json["{fname}"])' \
                    .format(fname=fname, type_class=type_name)
                dict_stmt = 'dict["{fname}"] = self.{fname}'.format(fname=fname)+".map{ $0.toDict() }"
            else:
                declare = ' let {fname}:[{type_class}]'.format(fname=fname,type_class=raw_type_class)
                stmt = '    self.{fname} = json["{fname}"].arrayObject as? [{type_class}] ?? []'\
                .format(fname=fname, type_class=raw_type_class)
        elif type_complex == 'd':
            tmp_value_stmt_tpl = '  let tmp_{fname}_value = json["{fname}"].{json_type}Value '
            json_type = "double"
            tmp_value_stmt = tmp_value_stmt_tpl.format(fname=fname, json_type=json_type)
            if ftype == 'di':
                field_value_stmt = '    self.{fname} = NSDate(timeIntervalSince1970: tmp_{fname}_value)'.format(fname=fname)
                stmt = '\n'.join([tmp_value_stmt, field_value_stmt])
                dict_stmt = '   dict["{fname}"] = self.{fname}.timeIntervalSince1970 '.format(fname=fname)
            elif ftype == 'ds':
                pass
    return declare, stmt, dict_stmt


def parse_line(line):
    field_infos = re.split(r',', line)
    stmts = []
    declares = []
    dict_stmts = []
    model_name = None
    for field_info in field_infos:
        field_info = field_info.strip()
        if not field_info:
            continue
        if field_info.startswith('-'):
            model_name = field_info[1:]
            continue
        declare, stmt, dict_stmt = parse_field_info(field_info)
        if declare and stmt and dict_stmt:
            declares.append(declare)
            stmts.append(stmt)
            dict_stmts.append(dict_stmt)

    return declares, stmts, dict_stmts,model_name


def main():
    declares = []
    stmts = []
    dict_stmts = []

    comments = []
    last_model_name = 'MyModel'
    for line in sys.stdin:
        line = line.strip()
        if line:
            comments.append("// "+line)
            declare_list, stmt_list, dict_stmt_list, model_name = parse_line(line)
            if model_name:
                last_model_name = model_name
            declares.extend(declare_list)
            stmts.extend(stmt_list)
            dict_stmts.extend(dict_stmt_list)
    declare_stmts = '\n'.join(declares)
    init_func_stmts = '\n'.join(stmts)
    to_dict_stmts = '\n'.join(dict_stmts)
    comment_stmts = '\n'.join(comments)

    model_class_tpl = Template("""
import SwiftyJSON
import BXModel
// Model Class Generated from templates
$comment_stmts
struct $model_name:BXModel {
    $declare_stmts

    required init(json:JSON){
        $init_func_stmts
    }

    func toDict() -> [String:AnyObject]{
      var dict : [String:AnyObject] = [ : ]
      $to_dict_stmts
      return dict
    }

}
    """)

    model_class_stmt = model_class_tpl.substitute(
        model_name=last_model_name,
        comment_stmts=comment_stmts,
        declare_stmts=declare_stmts,
        init_func_stmts=init_func_stmts,
        to_dict_stmts=to_dict_stmts
        )

    sys.stdout.write(model_class_stmt)

def json_to_fields():
    from . import converters
    input = sys.stdin.read()
    if isinstance(input,str):
        text = input.decode(encoding='utf-8')
    else:
        text = input
    fields = converters.convert_text_to_field_list(text)
    output = ','.join(fields)
    sys.stdout.write(output)


if __name__ == '__main__':
    main()
