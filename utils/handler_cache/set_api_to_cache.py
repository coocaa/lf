#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2022/3/28 16:08
# @Author : liuxw20
"""
import json
from typing import Dict
from jsonpath import jsonpath
from utils.handler_cache.cache_control import HandleCache


class SetApiToCache:
    """
    将用例中的请求或者响应内容存入缓存
    """

    def __init__(self, set_api_cache: Dict, case_data: Dict, response):
        self.set_api_cache = set_api_cache
        self.request_data = case_data
        self.response_data = response.text

    def set_main_caches(self, ):
        """
        设置缓存
        """
        if self.set_api_cache:
            for item in self.set_api_cache:
                expr = item['jsonpath']
                cache_name = item['cache_name']
                if item['depend_type'] == 'request':
                    self.set_request_cache(expr=expr, cache_name=cache_name)
                elif item['type'] == 'response':
                    self.set_response_cache(expr=expr, cache_name=cache_name)

    def set_request_cache(self, expr: str, cache_name: str) -> None:
        """
        将接口的请求参数存入缓存
        """
        _request_data = jsonpath(self.request_data, expr)

        if _request_data:
            HandleCache(cache_name).set_cache(_request_data[0])
        else:
            raise ValueError(
                "缓存设置失败，程序中未检测到需要缓存的数据。"
                f"请求数据: {self.request_data}"
                f"提取的jsonpath表达式为: {expr}")

    def set_response_cache(self, expr: str, cache_name: str) -> None:
        """
        将响应结果存入缓存
        """
        _response_data = jsonpath(json.loads(self.response_data), expr)
        if _response_data:
            HandleCache(cache_name).set_cache(_response_data[0])
        else:
            raise ValueError(
                "缓存设置失败，程序中未检测到需要缓存的数据。"
                f"响应数据: {self.response_data}"
                f"提取的jsonpath表达式为: {expr}")
