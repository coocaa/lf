#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 15:36
# @Author  : liuxw20
from enum import Enum


class RequestParamsEnum(Enum):
    """
    测试用例相关字段
    """
    # 用例描述
    TITLE = 'title'
    # 是否执行
    IS_RUN = 'is_run'
    # 接口url
    URL = 'url'
    # 请求方式
    METHOD = 'method'
    # 请求头
    HEADERS = 'headers'
    # token
    IS_TOKEN='is_token'


    # 请求数据--表单类型
    DATA = 'data'
    # 请求数据--路径类型
    PARAMS='params'
    # 请求数据--json类型
    JSON = 'json'
    # 请求数据--文件类型
    FILES = 'files'
    # 请求数据--导出类型
    EXPORT = 'export'


    # 断言内容
    ASSERT = 'assert'
    # sql内容
    SQL = 'sql'

    # 当前请求用例设置缓存
    SET_API_CACHE = "set_api_cache"

    # 前置sql
    SETUP_SQL = 'setup_sql'
    # 后置sql
    TEARDOWN_SQL = 'teardown_sql'

    # 后置清除
    TEARDOWN_CASE = "teardown_case"


    STATUS_CODE = "status_code"

    # 设置等待时间
    SLEEP = 'sleep'

    # 缓存数据存放
    RESPONSE_CACHE = 'response_cache'
