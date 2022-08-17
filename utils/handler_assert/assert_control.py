#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/7 17:48
# @Author  : liuxw20
import json
from typing import Text, Any, Union
from jsonpath import jsonpath
from utils.handler_assert import assert_type
from utils.handler_cache.update_case_cache import update_case_cache
from utils.handler_conf.get_conf_data import db_status
from utils.handler_enum.assert_method_enum import AssertMethodEnum
from utils.handler_log.log_control import log_error, log_warning
from utils.handler_other.common import load_module_func


class HandleAssert:
    """
    assert 断言模块封装,支持jsonpath方式的响应断言、数据库断言
    """

    def __init__(self, case_item: dict):

        self.assert_data = eval(update_case_cache(str(case_item['assert'])))
        self.funcs_mapping = load_module_func(assert_type)

    def handle_assert(self, res_info: dict) -> None:
        """
        assert 断言逻辑处理
        :param res_info: 请求的参数信息和响应内容
        :return:
        """
        response_data = res_info['response_data']
        sql_data = res_info['sql_data']
        status_code = res_info['status_code']

        if self.check_data_type(response_data, sql_data) is not False:
            if self.assert_data:
                for key, item in self.assert_data.items():
                    # 处理只断言状态的情况
                    if key == "status_code":
                        assert status_code == item
                    else:
                        assert_type = self.assert_data[key].pop('assert_type')
                        assert_jsonpath = self.assert_data[key].pop('jsonpath')
                        expect_value_expr = self.assert_data[key].items()

                        resp_data = jsonpath(json.loads(response_data), assert_jsonpath)
                        if resp_data:
                            # 先处理断言的方式和,要提取的预期结果jsonpath表达式
                            assert_method, expect_value_expr = self.get_expect_value_expr(expect_value_expr)
                            self.assert_type_handle(assert_type, sql_data, assert_method, expect_value_expr, item,
                                                    resp_data[0])
                        else:
                            log_error.logger.error(f"jsonpath提取失败！\n "
                                                   f""f"提取的数据: {response_data} \n "
                                                   f"表达式: {assert_jsonpath}")
                            raise ValueError(f"jsonpath提取失败！\n "
                                             f""f"提取的数据: {response_data} \n "
                                             f"表达式: {assert_jsonpath}")

    def check_data_type(self, response_data: str, sql_data: Union[dict, None]) -> None:
        """
        :param response_data: 响应数据
        :param sql_data: 数据库数据
        :return:
        """
        if response_data and sql_data:
            if isinstance(sql_data, dict):
                ...
            else:
                raise ValueError(
                    "断言失败，response_data、sql_data的数据类型必须要是字典类型，"
                    "请检查接口对应的数据是否正确\n"
                    f"sql_data: {sql_data}, 数据类型: {type(sql_data)}\n")

    def assert_type_handle(self, assert_type, sql_data, assert_method, expect_value_expr, item, resp_data) -> None:
        """
        处理断言类型
        :param assert_type: Union[str, None] 断言的类型是response 还是sql
        :param sql_data:    Union[str, None] sql
        :param assert_method:    断言方法
        :param expect_value_expr: Any,预期结果表达式
        :param item: 断言具体内容信息
        :param resp_data: jsonpath 提取的接口响应数据
        :param res_info: 响应全部内容
        :return:
        """
        if assert_type == 'db':
            self.type_is_sql(sql_data, assert_method, expect_value_expr, item, resp_data)

        elif assert_type is None or assert_type == 'response':
            assert_method_enum = AssertMethodEnum(assert_method).name
            self.funcs_mapping[assert_method_enum](resp_data, expect_value_expr)
        else:
            raise ValueError("断言错误!, 目前只支持数据库断言和响应断言")

    def type_is_sql(self, sql_data: dict, assert_method, expect_value_expr: Any, item: Any, resp_data: dict) -> None:
        """
        :param sql_data: 测试用例中的sql
        :param assert_method: 断言方法
        :param expect_value_expr: 预期结果表达式
        :param item:  断言的模块具体内容信息
        :param resp_data: jsonpath 提取的接口响应数据
        :return:
        """

        if db_status():
            if sql_data != {'sql': None}:
                sql_data_value = jsonpath(sql_data, expect_value_expr)
                if sql_data_value is False:
                    raise ValueError(
                        f"数据库断言内容jsonpath提取失败, 当前jsonpath表达式: {expect_value_expr}\n"
                        f"数据库返回数据: {sql_data}")

                sql_data_value = self.sql_data_is_bytes(sql_data_value[0])
                assert_method_enum = AssertMethodEnum(assert_method).name
                self.funcs_mapping[assert_method_enum](resp_data, sql_data_value)

            # 用例中未填写SQL
            else:
                raise ValueError("sql语句为空, 无法执行sql断言")
        else:
            log_warning.logger.warning(f"检测到数据库状态为关闭状态,程序已跳过此断言, 断言项: {item}")

    def sql_data_is_bytes(self, sql_data_value: Any) -> Text:
        """
        处理 mysql查询出来的数据类型如果是bytes类型，转换成str类型
        """
        if isinstance(sql_data_value, bytes):
            sql_data_value = sql_data_value.decode('utf=8')
        return sql_data_value

    def get_expect_value_expr(self, expect_value_expr) -> tuple:
        """
        处理断言的方式和,要提取的预期结果jsonpath表达式
        :param expect_value_expr:
        :return:
        """
        data = list(expect_value_expr)
        assert_method = data[0][0]
        expect_value_expr = data[0][1]

        return assert_method, expect_value_expr




if __name__ == '__main__':
    pass
