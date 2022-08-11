#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 11:22
# @Author  : liuxw20

"""
Assert 断言类型
"""

from typing import Any, Union, Text


def equal(actual_value: Any, expect_value: Any):
    """判断是否相等"""

    assert actual_value == expect_value


def less(actual_value: Union[int, float], expect_value: Union[int, float]):
    """判断实际结果小于预期结果"""
    assert actual_value < expect_value


def less_or_equal(actual_value: Union[int, float], expect_value: Union[int, float]):
    """判断实际结果小于等于预期结果"""
    assert actual_value <= expect_value


def greater(actual_value: Union[int, float], expect_value: Union[int, float]):
    """判断实际结果大于预期结果"""
    assert actual_value > expect_value


def greater_or_equal(actual_value: Union[int, float], expect_value: Union[int, float]):
    """判断实际结果大于等于预期结果"""
    assert actual_value >= expect_value


def not_equal(actual_value: Any, expect_value: Any):
    """判断实际结果不等于预期结果"""
    assert actual_value != expect_value


def string_equal(actual_value: Text, expect_value: Any):
    """判断字符串是否相等"""
    assert actual_value == expect_value


def length_equal(actual_value: Text, expect_value: int):
    """判断长度是否相等"""
    assert isinstance(expect_value, int), "expect_value 需要为 int 类型"
    assert len(actual_value) == expect_value


def length_greater(actual_value: Text, expect_value: Union[int, float]):
    """判断长度大于"""
    assert isinstance(expect_value, (float, int)), "expect_value 需要为 float/int 类型"

    assert len(str(actual_value)) > expect_value


def length_greater_or_equal(actual_value: Text, expect_value: Union[int, float]):
    """判断长度大于等于"""
    assert isinstance(expect_value, (int, float)), "expect_value 需要为 float/int 类型"
    assert len(actual_value) >= expect_value


def length_less(actual_value: Text, expect_value: Union[int, float]):
    """判断长度小于"""
    assert isinstance(expect_value, (int, float)), "expect_value 需要为 float/int 类型"
    assert len(actual_value) < expect_value


def length_less_or_equal(actual_value: Text, expect_value: Union[int, float]):
    """判断长度小于等于"""
    assert isinstance(expect_value, (int, float)), "expect_value 需要为 float/int 类型"
    assert len(actual_value) <= expect_value


def contains(actual_value: Any, expect_value: Any):
    """判断期望结果内容包含在实际结果中"""
    assert isinstance(
        actual_value, (list, tuple, dict, str, bytes)), "expect_value需要为 list/tuple/dict/str/bytes 类型"
    assert expect_value in actual_value


def contained_by(actual_value: Any, expect_value: Any):
    """判断实际结果包含在期望结果中"""
    assert isinstance(
        expect_value, (list, tuple, dict, str, bytes)), "expect_value 需要为  list/tuple/dict/str/bytes  类型"

    assert actual_value in expect_value


def startswith(actual_value: Any, expect_value: Any):
    """检查响应内容的开头是否和预期结果内容的开头相等"""
    assert str(actual_value).startswith(str(expect_value))


def endswith(actual_value: Any, expect_value: Any):
    """检查响应内容的结尾是否和预期结果内容相等"""
    assert str(actual_value).endswith(str(expect_value))
