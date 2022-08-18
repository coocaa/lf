#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/29 18:03
# @Author : liuxw20
from enum import Enum, unique


@unique
class SetApiCacheEnum(Enum):
    """
    设置当前接口至缓存枚举
    """
    # 当前请求用例设置缓存
    SET_API_CACHE = "set_api_cache"

    # jsonpath提取--jsonpath语法
    JSONPATH = 'jsonpath'
    # 缓存文件名
    CACHE_NAME = 'cache_name'
    # 依赖数据类型
    DEPEND_TYPE = 'depend_type'


    # 依赖用例的数据列表
    DEPEND_CASE_DATA = 'depend_case_data'
    # 依赖用例ID
    CASE_ID = 'case_id'
    # 具体依赖的数据
    DEPEND_DATA = 'depend_data'




