#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/29 18:03
# @Author : liuxw20
from enum import Enum, unique


@unique
class DependDataEnum(Enum):
    """
    数据依赖相关枚举
    """
    # 是否依赖用例
    IS_DEPEND = 'is_depend'
    # 依赖用例的数据列表
    DEPEND_CASE_DATA = 'depend_case_data'
    # 依赖用例ID
    CASE_ID = 'case_id'
    # 具体依赖的数据
    DEPEND_DATA = 'depend_data'
    # 依赖数据类型
    DEPEND_TYPE = 'depend_type'
    # jsonpath提取--jsonpath语法
    JSONPATH = 'jsonpath'

    # 替换的内容--也是jsonpath语法
    REPLACE_KEY = 'replace_key'

    # 依赖数据的类型---------------
    # 依赖响应中数据
    RESPONSE = 'response'
    # 依赖请求中的数据
    REQUEST = 'request'
    # 依赖sql中的数据
    SQL_DATA = 'sqlData'
    # 依赖存入缓存中的数据
    CACHE = "cache"

    # 设置当前提取的依赖数据到缓存中
    SET_CACHE='set_cache'