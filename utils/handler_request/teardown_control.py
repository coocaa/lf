#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2022/3/28 16:08
# @Author : liuxw20
"""

import json
from typing import Dict, Text
from jsonpath import jsonpath
from utils.handler_cache.cache_control import HandleCache
from utils.handler_conf.get_conf_data import db_status
from utils.handler_enum.request_params_enum import RequestParamsEnum
from utils.handler_jsonpath.jsonpath_control import jsonpath_replace, sql_regular
from utils.handler_log.log_control import log_error, log_warning
from utils.handler_mysql.mysql_control import HandleMysql
from utils.handler_request.request_control import HandleRequest


class HandlerTeardown:
    """
    处理yaml文件的后置请求
    """

    def handle_teardown(self, res_info: dict) -> None:
        """
        为什么在这里需要单独区分 param_prepare 和 send_request
        假设此时我们有用例A，teardown中我们需要执行用例B

        那么考虑用户可能需要获取获取teardown的用例B的响应内容，也有可能需要获取用例A的响应内容，
        因此我们这里需要通过关键词去做区分。这里需要考虑到，假设我们需要拿到B用例的响应，那么就需要先发送请求然后在拿到响应数据

        那如果我们需要拿到A接口的响应，此时我们就不需要在额外发送请求了，因此我们需要区分一个是前置准备param_prepare，
        一个是发送请求send_request

        @param res_info:
        @return:
        """
        teardown_case = res_info[RequestParamsEnum.TEARDOWN_CASE.value]
        if teardown_case:
            old_res_data = res_info['response_data']
            old_request_data = res_info['request_body']

            for data_item in teardown_case:
                if jsonpath(data_item, '$.param_ready'):
                    self.param_ready(data_item, old_res_data=json.loads(old_res_data))
                elif jsonpath(data_item, '$.send_request'):
                    self.send_request(data_item, old_request_data=old_request_data,
                                      old_res_data=json.loads(old_res_data))

        self.teardown_sql(res_info)

    def param_ready(self, data_item: Dict, old_res_data: Dict) -> None:
        """
        前置的请求参数处理
        :param data_item: 前置数据
        :param old_res_data:  响应数据
        :return:
        """

        cache_data = HandleCache.get_cases_cache(data_item['case_id'])
        if cache_data:
            res_info = self.teardown_http_requests(cache_data)

            param_ready = data_item['param_ready']
            for item in param_ready:
                if item['depend_type'] == 'self_response':
                    self.depend_type_is_self_response(teardown_case_data=item, old_res_data=old_res_data,
                                                      later_res_data=json.loads(res_info['response_data']))
        else:
            msg = f'teardown依赖的用例id不存在: {data_item["case_id"]} ,请检查'
            log_error.logger.error(msg)
            raise ValueError(msg)

    def send_request(self, data_item: Dict, old_request_data: Dict, old_res_data: Dict) -> None:
        """
        后置请求处理
        :param data_item:  后置请求测试数据
        :param old_request_data: 前置的请求数据
        :param old_res_data: 前置的响应数据
        :return:
        """
        cache_data = HandleCache.get_cases_cache(data_item['case_id'])
        if cache_data:
            _send_request = data_item['send_request']
            for item in _send_request:
                if item['depend_type'] == 'cache':
                    exec(self.depend_type_is_cache(teardown_case_data=item))
                if item['depend_type'] == 'response':
                    exec(self.depend_type_response(teardown_case_data=item, old_request_data=old_res_data))
                elif item['dependent_type'] == 'request':
                    self.dependent_type_request(teardown_case_data=item, old_request_data=old_request_data)
            self.teardown_http_requests(cache_data)
        else:
            msg = f'teardown依赖的用例id不存在: {data_item["case_id"]} ,请检查'
            log_error.logger.error(msg)
            raise ValueError(msg)

    @classmethod
    def teardown_http_requests(cls, cache_data: Dict) -> Dict:
        """
        发送后置请求的
        @param cache_data: 缓存中提取的后置用例
        @return:
        """

        res_info = HandleRequest().request(case_data=cache_data, dependent_switch=False)
        return res_info

    @classmethod
    def depend_type_is_self_response(cls, teardown_case_data: Dict, old_res_data: Dict, later_res_data: Dict) -> None:
        """
        处理依赖类型为依赖用例ID自己响应的内容
        :param : teardown_case_data: teardown中的用例数据
        :param : old_res_data:  之前用例接口的响应数据
        :param : later_res_data: 当前接口响应的内容
        :return:
        """
        try:
            set_cache_value_name = teardown_case_data['set_cache']
            _response_depend = jsonpath(later_res_data, expr=teardown_case_data['jsonpath'])
            if _response_depend:
                HandleCache.set_cache(set_cache_value_name, _response_depend[0])
            else:
                raise ValueError(
                    f"jsonpath提取失败，替换内容: {old_res_data} \n"
                    f"jsonpath表达式: {teardown_case_data['jsonpath']}")
        except KeyError as e:
            raise KeyError("teardown中缺少set_cache参数，请检查用例是否正确") from e

    @classmethod
    def depend_type_is_cache(cls, teardown_case_data: Dict) -> str:
        """
        判断依赖类型为从缓存中处理
        :param : teardown_case_data: teardown中的用例内容
        :return:
        """
        cache_name = teardown_case_data['cache_name']
        replace_key = teardown_case_data['replace_key']

        change_data = replace_key.split(".")  # $.data.applyId
        new_data = jsonpath_replace(change_data=change_data, key_name='teardown_case')

        # jsonpath 数据解析
        types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
        if any(i in cache_name for i in types) is True:
            cache_data=HandleCache.get_cache(cache_name.split(':')[1])
            new_data += f" = {cache_data}"

        # 最终提取到的数据,转换成 teardown_case[xxx][xxx]
        else:
            cache_data = HandleCache.get_cache(cache_name)
            new_data += f" = '{cache_data}'"

        return new_data

    @classmethod
    def depend_type_response(cls, teardown_case_data: Dict, old_request_data: Dict) -> str:
        """
        判断依赖类型为当前执行前置用例响应内容
        :param : teardown_case_data: teardown中的用例内容
        :param : old_request_data: 需要替换的内容
        :return:
        """
        replace_key = teardown_case_data['replace_key']
        response_depend = jsonpath(old_request_data, expr=teardown_case_data['jsonpath'])
        if response_depend:
            return cls.jsonpath_replace_data(replace_key=replace_key, replace_value=response_depend[0])
        else:
            raise ValueError(
                f"jsonpath提取失败，替换内容: {old_request_data} \n"
                f"jsonpath表达式: {teardown_case_data['jsonpath']}")

    @classmethod
    def dependent_type_request(cls, teardown_case_data: Dict, old_request_data: Dict) -> None:
        """
        判断依赖类型为请求的内容
        :param : teardown_case_data: teardown中的用例内容
        :param : old_request_data: 需要替换的内容
        :return:
        """
        try:
            request_set_value = teardown_case_data['set_value']
            request_depend = jsonpath(old_request_data, expr=teardown_case_data['jsonpath'])
            if request_depend:
                HandleCache.set_cache(request_set_value, request_depend[0])
            else:
                raise ValueError(
                    f"jsonpath提取失败，替换内容: {old_request_data} \n"
                    f"jsonpath表达式: {teardown_case_data['jsonpath']}")
        except KeyError as e:
            raise KeyError("teardown中缺少set_value参数，请检查用例是否正确") from e

    @classmethod
    def jsonpath_replace_data(cls, replace_key: str, replace_value: Dict) -> Text:
        """
        通过jsonpath判断出需要替换数据的位置
        """
        change_data = replace_key.split(".")
        new_data = jsonpath_replace(change_data=change_data, key_name='teardown_case')
        if not isinstance(replace_value, str):
            new_data += f" = {str(replace_value)}"

        # 最终提取到的数据,转换成 teardown_case[xxx][xxx]
        else:
            new_data += f" = '{replace_value}'"
        return new_data

    @classmethod
    def teardown_sql(cls, res_info: dict) -> None:
        """
        处理后置sql
        :param res_info:
        :return:
        """

        sql_data = res_info['teardown_sql']
        old_res_data = res_info['response_data']
        if sql_data:
            for item in sql_data:
                if db_status():
                    _sql_data = sql_regular(value=item, res_data=json.loads(old_res_data))
                    HandleMysql().insert_update_delete(_sql_data)
                else:
                    log_warning.logger.warning("程序中检测到数据库为关闭状态, 已跳过为执行sql: {}".format(item))
