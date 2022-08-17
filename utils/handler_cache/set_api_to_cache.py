#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2022/3/28 16:08
# @Author : liuxw20
"""
from typing import Dict
from utils.handler_cache.cache_control import HandleCache
from utils.handler_enum.set_api_cache_enum import SetApiCacheEnum
from utils.handler_jsonpath.jsonpath_control import get_value_by_jsonpath


class SetApiToCache:
    """
    将用例中的请求或者响应内容存入缓存
    """

    def __init__(self, set_api_cache: Dict, case_data: Dict, response):
        self.set_api_cache = set_api_cache
        self.request_data = case_data
        self.response_data = response.text

    def set_main_caches(self):
        """
        设置缓存
        """
        if self.set_api_cache:
            for item in self.set_api_cache:
                expr = item[SetApiCacheEnum.JSONPATH.value]
                cache_name = item[SetApiCacheEnum.CACHE_NAME.value]
                if item[SetApiCacheEnum.DEPEND_TYPE.value] == 'request':
                    self.set_request_cache(expr=expr, cache_name=cache_name)
                elif item[SetApiCacheEnum.DEPEND_TYPE.value] == 'response':
                    self.set_response_cache(expr=expr, cache_name=cache_name)

    def set_request_cache(self, expr: str, cache_name: str) -> None:
        """
        将接口的请求参数存入缓存
        """
        _request_data = get_value_by_jsonpath(self.request_data, expr)
        HandleCache.set_cache(cache_name, _request_data)

    def set_response_cache(self, expr: str, cache_name: str) -> None:
        """
        将响应结果存入缓存
        """
        _response_data = get_value_by_jsonpath(self.response_data, expr)
        HandleCache.set_cache(cache_name, _response_data)
