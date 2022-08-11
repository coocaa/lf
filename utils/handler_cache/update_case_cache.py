#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/7 15:22
# @Author  : liuxw20
import re

from utils.handler_cache.cache_control import HandleCache
from utils.handler_log.log_control import log_error


def update_case_cache(data:str) -> dict:
    """
    通过正则的方式，更新用例中需要的缓存中的数据
    :param data:
    :return:
    """

    regular_list = re.findall(r'cache\(.+?\)', data)


    for item in regular_list:
        start_index = item.find('(')
        end_index = item.rfind(')')
        cache_name = item[start_index + 1:end_index]

        # 生成表达式
        pattern = re.compile(r'cache\(' + cache_name + '\)')
        try:
            _cache_data = HandleCache(filename=cache_name).get_cache()
            #使用sub方法，替换已经拿到的内容
            data = re.sub(pattern, _cache_data, data)
        except Exception:
            log_error.logger.error('更新缓存数据失败,请检查')

    return data




