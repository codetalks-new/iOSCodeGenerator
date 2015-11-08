# -*- coding: utf-8 -*-
__author__ = 'banxi'
import sys
import re
from string import Template


char_type_map = {
    's': 'String',
    'i': 'Int',
    'f': 'Double',
    'b': 'Bool',
    'di': 'NSDate',
    'ds': 'NSDate',
}


def parse_field_info(field_info):
    parts = re.split(':', field_info.strip())
    fname = parts[0]
    ftype = None
    if len(parts) > 1:
        ftype = parts[1]
    if not ftype:
        ftype = 's'
    type_class = char_type_map.get(ftype, 'String')
    declare = '    let {fname}:{type_class} '.format(fname=fname, type_class=type_class)
    stmt = None
    dict_stmt = None
    if len(ftype) == 1:
        json_type = type_class.lower()
        stmt = '    self.{fname} = json["{fname}"].{json_type}Value'.format(fname=fname, json_type=json_type)
        dict_stmt = '   dict["{fname}"] = self.{fname}'.format(fname=fname)
    elif len(ftype) == 2:
        tmp_value_stmt_tpl = '  let tmp_{fname}_value = json["{fname}"].{json_type}Value '
        type_char = ftype[1]
        raw_type_class = char_type_map.get(type_char, 'String')
        json_type = raw_type_class.lower()
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
    for field_info in field_infos:
        if not field_info:
            continue
        declare, stmt, dict_stmt = parse_field_info(field_info)
        if declare and stmt and dict_stmt:
            declares.append(declare)
            stmts.append(stmt)
            dict_stmts.append(dict_stmt)

    return declares, stmts, dict_stmts


def main():
    declares = []
    stmts = []
    dict_stmts = []

    comments = []
    for line in sys.stdin:
        if line:
            comments.append("// "+line)
            declare_list, stmt_list, dict_stmts = parse_line(line)
            declares.extend(declare_list)
            stmts.extend(stmt_list)
            dict_stmts.extend(dict_stmts)
    declare_stmts = '\n'.join(declares)
    init_func_stmts = '\n'.join(stmts)
    to_dict_stmts = '\n'.join(dict_stmts)
    comment_stmts = '\n'.join(comments)

    model_class_tpl = Template("""
// Model Class Generated from templates
$comment_stmts
class MyModel {
    $declare_stmts

    init(json:JSON){
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
        comment_stmts=comment_stmts,
        declare_stmts=declare_stmts,
        init_func_stmts=init_func_stmts,
        to_dict_stmts=to_dict_stmts
        )

    sys.stdout.write(model_class_stmt)

if __name__ == '__main__':
    main()
