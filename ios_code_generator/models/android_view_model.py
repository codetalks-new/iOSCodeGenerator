# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.generators import as_android_kotlin_generator
from ios_code_generator.models import Field
from ios_code_generator.models import Model

__author__ = 'banxi'

class AndroidViewField(Field):
    pass

@as_android_kotlin_generator("view")
class AndroidViewModel(Model):
    field_class = AndroidViewField




ui_field_type_map = {
    'l': 'TextView',
    'b': 'Button',
    'ib': 'ImageButton',
    'v': 'View',
    'i': 'ImageView',
    'f': 'EditText',
    's': 'ListView',
    'p': 'UIPickerView',
    'cb': 'CheckboxButton',
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