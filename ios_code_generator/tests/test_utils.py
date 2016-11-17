# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ios_code_generator.utils import to_mixed_case, to_camel_case

__author__ = 'banxi'


def test_to_mixed_case():  # noqa
    assert to_mixed_case('user') == 'user'
    assert to_mixed_case('User') == 'user'
    assert to_mixed_case('userStory') == 'userStory'
    assert to_mixed_case('UserStory') == 'userStory'
    assert to_mixed_case('User-Story') == 'userStory'
    assert to_mixed_case('User_Story') == 'userStory'
    assert to_mixed_case('User Story') == 'userStory'
    assert to_mixed_case('user story') == 'userStory'


def test_to_camel_case():  # noqa
    assert to_camel_case('user') == 'User'
    assert to_camel_case('User') == 'User'
    assert to_camel_case('userStory') == 'UserStory'
    assert to_camel_case('UserStory') == 'UserStory'
    assert to_camel_case('User-Story') == 'UserStory'
    assert to_camel_case('User_Story') == 'UserStory'
    assert to_camel_case('User Story') == 'UserStory'
    assert to_camel_case('user story') == 'UserStory'
