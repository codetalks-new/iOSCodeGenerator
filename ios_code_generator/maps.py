# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'banxi'
ui_field_type_map = {
    'l': 'UILabel',
    'b': 'UIButton',
    'v': 'UIView',
    'i': 'UIImageView',
    'f': 'UITextField',
    'ct': 'UIControl',
    't': 'UITableView',
    's': 'UIScrollView',
    'c': 'UICollectionView',
    'cr': 'UICollectionReusableView',
    'p': 'UIPickerView',
    'cb': 'CheckboxButton',
    'ib': 'IconButton',
    'vib': 'VerticalIconButton',
    'ob': 'OutlineButton',
    'sb': 'UISearchBar',
    'pc': 'UIPageControl',
    'dp': 'UIDatePicker',
    'st': 'UIStepper',
    'sw': 'UISwitch',
    'sl': 'UISlider',
    'sc': 'UISegmentedControl',
    'tc': 'UITableViewCell',
    'thf': 'UITableViewHeaderFooterView',
    'stc': 'AppStaticCell',
    'ltc': 'LabelTextCell',
    'ltvc': 'LabelTextViewCell',
    'lsc': 'LabelSpanCell',
    'rdc': 'AppRightDetailCell',
    'src': 'StarRatingControl',
    'tb': 'UIToolbar',
    'ctb': 'ConfirmTitleBar',
    'tv': 'UITextView',
    'il': 'IconLabel',
    'ol': 'OvalLabel',
    'ci': 'OvalImageView',
    'wv': 'WKWebView',
    'uwv': 'UIWebView',
    'gbb': 'GroupButtonBar',
    'oi': 'OutlineImageView'
}

ui_field_custom_type_pure_name = {
    "ib": "Button",
    "cb": "Button",
    "vib": "Button",
    "ob": "Button",
    "il": "Label",
    "ol": "Label",
    "ci": "ImageView",
    "oi": "ImageView",
}

ui_image_field_types = [
    'i', 'oi', 'ci'
]
ui_button_field_types = [
    'b', 'cb', 'ib', 'ob'
]

ui_has_textColor_prop_field_types = [
    'l', 'il', 'ol', 'f', 'tv',
]
ui_has_textColor_prop_field_types += ui_button_field_types

ui_prefer_tintColor_prop_field_types = [
    'i', 'f', 'sb', 'pc', 'dp', 'sb', 'st', 'sw', 'sl', 'src', 'ctb',
]

ui_prefer_tintColor_prop_field_types += ui_button_field_types

ui_type_value_field_map = {
    'l': 'text',
    'f': 'text',
    'il': 'text',
    'ol': 'text',
    'sw': 'on',
    'tv': 'text',
}
ui_type_value_type_map = {
    'l': 'String',
    'il': 'String',
    'ol': 'String',
    'f': 'String',
    'tv': 'String',
    'sw': 'Bool'
}
ui_view_designed_init_map = {
    'b': 'UIButton(type:.system)',
    'c': ' UICollectionView(frame: .zero, collectionViewLayout: UICollectionViewFlowLayout())',
    'sb': 'UISearchBar()',
    'gbb': 'GroupButtonBar(buttons:[])',
    'il': 'IconLabel(iconPosition:  .left)'
}
ui_model_type_map = {
    'v': 'UIView',
    't': 'UITableView',
    's': 'UIScrollView',
    'c': 'UICollectionView',
    'ct': 'UIControl',
    'tc': 'UITableViewCell',
    'stc': 'StaticTableViewCell',
    'cc': 'UICollectionViewCell',
}

ui_controller_model_type_map = {
    'vc': 'BaseUIViewController',
    'tvc': 'BaseUITableViewController',
    'cvc': 'BaseUICollectionViewController',
    'tabvc': 'BaseUITabBarController',
}
ui_field_attr_map = {
    'f': '%UIFont.systemFont(ofSize:%s)',
    'fb': 'UIFont.boldSystemFont(ofSize:%s)',
    'cdg': '+.darkGray',
    'cdt': '+.darkText',
    'cg': '+.gray',
    'clg': '+.lightGray',
    'cb': '+.black',
    'cblue': '+.blue',
    'cw': '+.white',
    'cdgt': '+.darkGray',
    'cpt': '+.primaryText',
    'cst': '+.secondaryText',
    'ctt': '+.tertiaryText',
    'cht': '+.hintText',
    'cwa': '+UIColor(white: 1.0, alpha: 1.0)',
    'ch': '%UIColor(hex:%s)',
    'ca': '+.accent',
    'cp': '+.primary',
    'cr': '+.red',
    'bp': '+setBackgroundImage(Asset.buttonPrimary.image,for:.normal)'
}
ui_field_attr_sketch_map = {
    'btc': 'barTintColor',
    'tint': 'tintColor',
    'color': 'textColor',
    'bgc': 'backgroundColor',
    'bg': 'backgroundColor'
}

enum_raw_type_map = {
    'i': 'Int',
    's': 'String'
}
settings_raw_type_map = {
    'i': 'Int',
    's': 'String',
    'b': 'Bool',
    'f': 'Double',
    'u': 'URL',
    'd': 'Date',
}

ui_field_pa_map = {
    'x': 'pa_centerX',
    'y': 'pa_centerY',
    'l': 'pa_leading',
    'lm': 'pa_leadingMargin',
    't': 'pa_top',
    'tm': 'pa_topMargin',
    'r': 'pa_trailing',
    'rm': 'pa_trailingMargin',
    'b': 'pa_bottom',
    'bm': 'pa_bottomMargin',
    'w': 'pa_width',
    'h': 'pa_height',
    'a': 'pac_aspectRatio',
    'e': 'pac_edge',
    'hor': 'pac_horizontal',
    'ver': 'pac_vertical',
    'bl': 'pa_below',
    'ab': 'pa_above',
    'bf': 'pa_before',
    'at': 'pa_after',
}
ui_field_pa_relative_layout_map = {
    'bl': 'pa_below',
    'ab': 'pa_above',
    'bf': 'pa_before',
    'at': 'pa_after',
}
ui_field_pa_relation_map = {
    '=': 'eq',
    '>': 'gte',
    '<': 'lte',
}
ui_vc_pa_func_map = {
    't': 'pa_below(self.topLayoutGuide)',
    'b': 'pa_above(self.bottomLayoutGuide)'
}

db_type_map = {
    's': 'String',
    'i': 'Int',
    'b': 'Bool',
    'f': 'Double',
    'j': 'JSON',
    'u': 'URL',
    'd': 'Date',
    'di': 'Date'
}

m_char_type_map = {
    's': 'String',
    'i': 'Int',
    'i32': 'Int32',
    'i64': 'Int64',
    'ui64': 'UInt64',
    'ui8': 'UInt8',
    'l': 'Int64',
    'f': 'Double',
    'd': 'Double',
    'b': 'Bool',
    'u': 'URL?',
    'r': 'Ref',
    'j': 'JSON',
    'di': 'Date',
    'ds': 'Date',
    '[s': 'Array',
    '[u': 'Array',
    '[i': 'Array',
    '[f': 'Array',
    '[d': 'Array',
    '[b': 'Array',
    '[r': 'RefArray'
}

m_kotlin_char_type_map = {
    's': 'String',
    'i': 'Int',
    'f': 'Float',
    'd': 'Double',
    'b': 'Boolean',
    'u': 'Uri',
    'r': 'Ref',
    'j': 'JSONObject',
    'di': 'Date',
    'ds': 'Date',
    '[s': 'Array<String>',
    '[u': 'Array<Uri>',
    '[i': 'Array<Int>',
    '[f': 'Array<Double>',
    '[d': 'Array<Double>',
    '[b': 'Array<Boolean>',
    '[r': 'RefArray'
}
