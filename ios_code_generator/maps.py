# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'banxi'
ui_field_type_map = {
    'l': 'UILabel',
    'b': 'UIButton',
    'v': 'UIView',
    'i': 'UIImageView',
    'f': 'UITextField',
    't': 'UITableView',
    's': 'UIScrollView',
    'c': 'UICollectionView',
    'cr': 'UICollectionReusableView',
    'p': 'UIPickerView',
    'cb': 'CheckboxButton',
    'ib': 'IconButton',
    'sb': 'UISearchBar',
    'pc': 'UIPageControl',
    'dp': 'UIDatePicker',
    'st': 'UIStepper',
    'sw': 'UISwitch',
    'sl': 'UISlider',
    'sc': 'UISegmentedControl',
    'tc': 'UITableViewCell',
    'stc': 'StaticTableViewCell',
    'src': 'StarRatingControl',
    'tb': 'UIToolbar',
    'ctb': 'ConfirmTitleBar',
    'tv': 'UITextView',
    'il': 'IconLabel',
    'ci': 'OvalImageView',
    'wv': 'WKWebView',
    'gbb': 'GroupButtonBar',
    'oi': 'OutlineImageView'
}


ui_image_field_types = [
    'i','oi','ci'
]
ui_button_field_types = [
    'b','cb','ib'
]

ui_has_textColor_prop_field_types = [
    'l','il','f',
]
ui_has_textColor_prop_field_types += ui_button_field_types

ui_prefer_tintColor_prop_field_types = [
    'i','f','sb','pc','dp','sb','st','sw','sl','src','ctb',
]

ui_prefer_tintColor_prop_field_types += ui_button_field_types

ui_type_value_field_map = {
    'l': 'text',
    'f': 'text',
    'sw': 'on',
}
ui_type_value_type_map = {
    'l': 'String',
    'f': 'String',
    'sw': 'Bool'
}
ui_view_designed_init_map = {
    'b': 'UIButton(type:.System)',
    'c': ' UICollectionView(frame: CGRectZero, collectionViewLayout: UICollectionViewFlowLayout())',
    'sb': 'UISearchBar()',
    'gbb': 'GroupButtonBar(buttons:[])'
}
ui_model_type_map = {
    'v': 'UIView',
    't': 'UITableView',
    's': 'UIScrollView',
    'c': 'UICollectionView',
    'tc': 'UITableViewCell',
    'stc': 'StaticTableViewCell',
    'cc': 'UICollectionViewCell',
    'vc': 'BaseUIViewController',
    'tvc': 'BaseUITableViewController',
    'tabvc': 'BaseUITabBarController',
}
ui_field_attr_map = {
    'f': 'UIFont.systemFontOfSize',
    'fb': 'UIFont.boldSystemFontOfSize',
    'cdg': '+UIColor.darkGrayColor()',
    'cdt': '+UIColor.darkTextColor()',
    'cdgt': '+AppColors.darkGrayTextColor',
    'cpt': '+AppColors.primaryTextColor',
    'cst': '+AppColors.secondaryTextColor',
    'ctt': '+AppColors.tertiaryTextColor',
    'cht': '+AppColors.hintTextColor',
    'cg': '+UIColor.grayColor()',
    'clg': '+UIColor.lightGrayColor()',
    'cb': '+UIColor.blackColor()',
    'cw': '+UIColor.whiteColor()',
    'cwa': '+UIColor(white: 1.0, alpha: 1.0)',
    'ch': '+UIColor(hex:0xabc)',
    'ca': '+AppColors.accentColor',
    'bp': '+setBackgroundImage(UIImage.Asset.ButtonPrimary.image,forState:.Normal)'
}
ui_field_attr_sketch_map = {
    'btc':'barTintColor',
    'tint':'tintColor',
    'color':'textColor',
    'bgc':'backgroundColor'
}

enum_raw_type_map = {
    'i': 'Int',
    's': 'String'
}
settings_raw_type_map = {
    'i':'Int',
    's':'String',
    'b': 'Bool',
    'f': 'Double',
    'u': 'NSURL',
    'd': 'NSDate',
}
ui_field_pin_map = {
    'x': 'pinCenterX',
    'y': 'pinCenterY',
    'l': 'pinLeading',
    't': 'pinTop',
    'r': 'pinTrailing',
    'b': 'pinBottom',
    'w': 'pinWidth',
    'h': 'pinHeight',
    'a': 'pinAspectRatio',
    'e': 'pinEdge',
    'hor': 'pinHorizontal',
    'ver': 'pinVertical',
}
ui_field_pa_map = {
    'x': 'pa_centerX',
    'y': 'pa_centerY',
    'l': 'pa_leading',
    't': 'pa_top',
    'r': 'pa_trailing',
    'b': 'pa_bottom',
    'w': 'pa_width',
    'h': 'pa_height',
    'a': 'pac_aspectRatio',
    'e': 'pac_edge',
    'hor': 'pac_horizontal',
    'ver': 'pac_vertical',
    'bl':'pa_below',
    'ab':'pa_above',
    'bf':'pa_before',
    'at':'pa_after',
}
ui_field_pa_relative_layout_map = {
    'bl':'pa_below',
    'ab':'pa_above',
    'bf':'pa_before',
    'at':'pa_after',
}
ui_field_pa_relation_map = {
    '=':'eq',
    '>':'gte',
    '<':'lte',
}
ui_vc_pa_func_map = {
    't': 'pa_below(self.topLayoutGuide)',
    'b': 'pa_above(self.bottomLayoutGuide)'
}