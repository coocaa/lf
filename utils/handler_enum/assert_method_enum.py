#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/29 18:03
# @Author : liuxw20

from enum import Enum, unique


@unique
class AssertMethodEnum(Enum):
    # 是否相等
    equal = "=="
    # 判断实际结果小于预期结果
    less = "lt"
    # 判断实际结果小于等于预期结果
    less_or_equal = "le"
    # 判断实际结果大于预期结果
    greater = "gt"
    # 判断实际结果大于等于预期结果
    greater_or_equal = "ge"
    # 判断实际结果不等于预期结果
    not_equal = "not_eq"
    # 判断字符串是否相等
    string_equals = "str_eq"
    # 判断长度是否相等
    length_equal = "len_eq"
    # 判断长度大于
    length_greater = "len_gt"
    # 判断长度大于等于
    length_greater_or_equal = 'len_ge'
    # 判断长度小于
    length_less = "len_lt"
    # 判断长度小于等于
    length_less_or_equal = 'len_le'
    # 判断期望结果内容包含在实际结果中
    contains = "contains"
    # 判断实际结果包含在期望结果中
    contained_by = 'contained_by'
    # 检查响应内容的开头是否和预期结果内容的开头相等
    startswith = 'startswith'
    # 检查响应内容的结尾是否和预期结果内容相等
    endswith = 'endswith'
