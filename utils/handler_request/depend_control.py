#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2022/3/28 16:08
# @Author : liuxw20
"""

import json
from typing import Dict
from utils.handler_cache.cache_control import HandleCache
from utils.handler_jsonpath.jsonpath_control import get_value_by_jsonpath, jsonpath_replace
from utils.handler_request.request_control import HandleRequest
from utils.handler_log.log_control import log_error
from utils.handler_enum.depend_data_enum import DependDataEnum
from utils.handler_enum.request_params_enum import RequestParamsEnum


class HandleDepend:
    """
    处理依赖相关的业务
    """

    def get_depend_data(self, case_data: Dict, sql_result) -> None:
        """
        jsonpath 和 依赖的数据,进行替换
        @param case_data:
        @param sql_result:
        """

        expr_and_value = self.analysis_depend(case_data, sql_result)
        for key, value in expr_and_value.items():
            change_data = key.split(".")  # key=$.data.token
            new_data = jsonpath_replace(change_data=change_data, key_name='case_data')
            new_data += f'={value}'
            exec(new_data)

    def analysis_depend(self, case_data: Dict, sql_result: Dict) -> dict:
        """
        解析依赖的数据
        :return:
        """

        depend_case_data = case_data[DependDataEnum.DEPEND_CASE_DATA.value]  # list类型

        expr_and_value = {}
        try:
            for depend_item in depend_case_data:
                case_id = depend_item[DependDataEnum.CASE_ID.value]
                if case_id == 'self':
                    self.depend_type_is_sql(sql_result, depend_item, expr_and_value, case_data)

                else:
                    cache_case = self.get_cache_data(case_id)
                    res_info = HandleRequest().request(cache_case)
                    depend_data = depend_item.get(DependDataEnum.DEPEND_DATA.value)

                    if depend_data:
                        for item in depend_data:
                            depend_type = item[DependDataEnum.DEPEND_TYPE.value]
                            jsonpath_expr = item[DependDataEnum.JSONPATH.value]
                            replace_key_value = item.get(DependDataEnum.REPLACE_KEY.value)
                            set_cache_value = item.get(DependDataEnum.SET_CACHE.value)

                            # 处理依赖数据类型是 response
                            if depend_type == DependDataEnum.RESPONSE.value:
                                self.other_depend_type(
                                    depend_type=0,
                                    case_data=case_data,
                                    expr_and_value=expr_and_value,
                                    res_data=json.loads(res_info['response_data']),
                                    expr=jsonpath_expr,
                                    set_cache_value=set_cache_value,
                                    replace_key=replace_key_value)

                            # 处理依赖数据类型是 request
                            elif depend_type == DependDataEnum.REQUEST.value:
                                self.other_depend_type(
                                    depend_type=1,
                                    case_data=case_data,
                                    expr_and_value=expr_and_value,
                                    res_data=res_info.get('request_body'),
                                    expr=jsonpath_expr,
                                    set_value=set_cache_value,
                                    replace_key=replace_key_value)

                            else:
                                log_error.logger.error(
                                    "当前用例的depend_type不正确，目前只支持request、response、db依赖\n"
                                    f"当前填写内容: {item[DependDataEnum.DEPEND_TYPE.value]}")
                                raise ValueError(
                                    "当前用例的depend_type不正确，目前只支持request、response、db依赖\n"
                                    f"当前填写内容: {item[DependDataEnum.DEPEND_TYPE.value]}")

            return expr_and_value

        except KeyError as exc:
            log_error.logger.error(
                f"depend_case_data依赖数据中，未找到 {exc} 参数，请检查是否填写\n"
                f"如已填写，请检查是否存在yaml缩进问题")
            raise KeyError(
                f"depend_case_data依赖数据中，未找到 {exc} 参数，请检查是否填写\n"
                f"如已填写，请检查是否存在yaml缩进问题") from exc

        except TypeError as exc:
            log_error.logger.error("请检查相关数据是否填写, 如已填写, 请检查缩进问题")
            raise TypeError("请检查相关数据是否填写, 如已填写, 请检查缩进问题") from exc


    @classmethod
    def depend_type_is_sql(cls, sql_result: Dict, depend_item: Dict, expr_and_value: Dict, case_data: Dict) -> None:
        """
        处理依赖类型为 sql，则依赖数据从数据库中提取
        :param sql_result: 执行后的sql结果
        :param depend_item: 具体的依赖数据-- 多组
        :param expr_and_value: 存放
        :param case_data: 所有测试数据
        :return:
        """

        if sql_result != {}:
            depend_data = depend_item[DependDataEnum.DEPEND_DATA.value]
            for item in depend_data:

                value = get_value_by_jsonpath(sql_result, item[DependDataEnum.JSONPATH.value])

                cache_name = item.get(DependDataEnum.SET_CACHE.value)
                if cache_name:
                    HandleCache(filename=cache_name).set_cache(value)

                replace_key_value = item.get([DependDataEnum.REPLACE_KEY.value])
                if replace_key_value:
                    expr_and_value[replace_key_value] = value
                    cls.replace_url(replace_key_value, expr_and_value, value, case_data)

        else:
            log_error.logger.error("检测到你在使用数据库字段，但是setup_sql中未查询出任何数据")

    @classmethod
    def other_depend_type(cls, depend_type, case_data, expr_and_value, res_data, expr, replace_key, set_cache_value) -> None:
        """
        处理数据替换
        :param depend_type:
        :param case_data:
        :param expr_and_value:
        :param res_data:
        :param expr:
        :param replace_key:
        :param set_cache_value:
        :return:
        """
        value = get_value_by_jsonpath(res_data, expr)
        if set_cache_value:
            HandleCache(filename=set_cache_value).set_cache(value)
        if replace_key:
            if depend_type == 0:
                expr_and_value[replace_key] = value

            cls.replace_url(replace_key, expr_and_value, value, case_data)

    @classmethod
    def replace_url(cls, replace_key: str, expr_and_value: dict, value: str, case_data: dict) -> None:
        """
        url中的动态参数替换
        # 如: 一般有些接口的参数在url中,并且没有参数名称, /api/v1/work/spu/approval/spuApplyDetails/{id}
        # 那么可以使用如下方式编写用例, 可以使用 $url_params{}替换,
        # 如/api/v1/work/spu/approval/spuApplyDetails/$url_params{id}
        :param replace_key: jsonpath表达式
        :param expr_and_value: 替换的表达式和值
        :param value: jsonpath提取的值
        :param case_data: 用例数据
        :return:
        """

        if "$url_param" in replace_key:
            _url = case_data['url'].replace(replace_key, str(value))
            expr_and_value['$.url'] = _url
        else:
            expr_and_value[replace_key] = str(value)

    @classmethod
    def get_cache_data(cls, case_id: str) -> Dict:
        """
        通过 case_id 获取缓存文件中的用例数据，
        :param case_id:
        :return:
        """
        # 安全的方式读取缓存文件中的数据
        # cache_data = ast.literal_eval(HandleCache('cases_cache.json').get_cache())[case_id]
        try:
            cache_data = HandleCache('cases_cache.json').get_json_cache()[case_id]
            return cache_data
        except KeyError as e:
            log_error.logger.error(f'依赖的用例id不存在: {case_id} ,请检查')
            raise KeyError(f'依赖的用例id不存在: {case_id} ,请检查')
