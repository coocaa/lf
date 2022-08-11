#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/6 13:56
# @Author  : liuxw20
import json
import re
import jsonpath
from utils.handler_log.log_control import log_error


def get_value_by_jsonpath(data: dict, expr: str) -> str:
    """
    通过jsonpath提取依赖的数据
    :param data: 提取的数据对象
    :param expr: 表达式
    :return: 提取到的内容值
    """
    if isinstance(data, dict):
        try:
            value = jsonpath.jsonpath(data, expr)[0]
            return value
        except Exception as e:
            log_error.logger.error(f"jsonpath提取失败！\n "f"提取的数据: {data} \n " f"表达式: {expr}")
            raise ValueError(f"jsonpath提取失败！\n "f"提取的数据: {data} \n " f"表达式: {expr}")
    else:
        # 将json格式的字符串,转化为字典--反序列化
        try:
            value = jsonpath.jsonpath(data, expr)[0]
            return value
        except Exception as e:
            log_error.logger.error(f"jsonpath提取失败！\n "f"提取的数据: {data} \n " f"表达式: {expr}")
            raise ValueError(f"jsonpath提取失败！\n "f"提取的数据: {data} \n " f"表达式: {expr}")


def jsonpath_replace(change_data, key_name):
    """
    处理replace_key 的替换逻辑
    :param change_data: [$,data,token]
    :param key_name:    case_data
    :return:            case_data['data']['token']
    """
    data = key_name
    for i in change_data:
        if i == '$':
            pass
        elif i[0] == '[' and i[-1] == ']':
            data += "[" + i[1:-1] + "]"
        else:
            data += "['" + i + "']"

    return data


def sql_regular(sql, res_data=None):
    """
    这里处理sql中的依赖数据，通过获取接口响应的jsonpath的值进行替换
    :param res_data: 接口响应数据, json格式
    :param value:
    :return:
    """
    sql_json_list = re.findall(r"\$json\((.*?)\)\$", sql)

    for i in sql_json_list:
        pattern = re.compile(r'\$json\(' + i.replace('$', "\$").replace('[', '\[') + r'\)\$')
        key = str(sql_json(i, res_data))
        sql = re.sub(pattern, key, sql, count=1)

    return sql


def sql_json(js_path, res_data):
    """ 提取 sql中的 json 数据 """
    _json_data = jsonpath(res_data, js_path)[0]
    if _json_data is not False:
        raise ValueError(f"sql中的jsonpath获取失败 {res_data}, {js_path}")
    return jsonpath(res_data, js_path)[0]


def get_value(data, key=None):
    """
    封装提取响应json数据和测试数据中指定key的value
    :param data: 响应json数据或测试数据
    :param key:  要提取的key
    :return:
    """
    if isinstance(data, dict):
        value = jsonpath.jsonpath(data, f'$..{key}')
        return value

    else:
        # 将json格式的字符串,转化为字典--反序列化
        value = jsonpath.jsonpath(json.loads(data), f'$..{key}')
        return value

