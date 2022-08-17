#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2022/3/28 12:52
# @Author : liuxw20
"""

import datetime
import decimal
import pymysql
from warnings import filterwarnings
from typing import List, Union, Dict
from utils.handler_conf.conf_control import conf
from utils.handler_conf.get_conf_data import db_status
from utils.handler_jsonpath.jsonpath_control import sql_regular
from utils.handler_log.log_control import log_error, log_warning

filterwarnings("ignore", category=pymysql.Warning)  # 忽略 Mysql 告警信息


class HandleMysql:
    """
    封装操作数据库
    """
    if db_status():
        def __init__(self):
            try:
                self.connect = pymysql.connect(
                    host=conf.get('mysql', 'host'),
                    port=conf.get('mysql', 'port'),
                    user=conf.get('mysql', 'user'),
                    password=conf.get('mysql', 'password'),
                    database=conf.get('mysql', 'database'),
                    cursor=pymysql.cursors.DictCursor,  # 字典游标
                    charset='utf8')

                self.cur = self.connect.cursor()
            except AttributeError as e:
                log_error.logger.error("数据库连接失败, 失败原因: {e}".format(e))

        def __del__(self):
            # 清理对象
            try:
                self.cur.close()
                self.connect.close()
            except AttributeError as e:
                log_error.logger.error("数据库连接失败, 失败原因: {e}".format(e))

        def query(self, sql: str, state="all") -> dict:
            """返回所有数据"""
            self.cur.execute(sql)
            data = self.cur.fetchall()
            return data

        def insert_update_delete(self, sql: str) -> str:
            """"增删改操作"""
            try:
                rows = self.cur.execute(sql)
                self.connect.commit()
                return rows

            except AttributeError as e:
                log_error.logger.error("数据库执行sql异常, 失败原因: {e}".format(e))
                self.connect.rollback()
                raise


class SetupMysql(HandleMysql):
    """
    处理前置sql
    """

    def get_setup_sql_data(self, sql_list: Union[List, None]) -> Dict:
        """
        处理前置请求sql_list
        :param sql_list:
        :return:
        """
        try:
            result = {}
            if db_status():
                if sql_list:
                    for item in sql_list:
                        # 判断sql是查询
                        if item[0:6].upper() == 'SELECT':
                            sql_data = self.query(sql=item)[0]
                            for key, value in sql_data.items():
                                result[key] = value
                        else:
                            self.insert_update_delete(sql=item)
            else:
                log_warning.logger.warning("数据库状态未开启,请检查配置")
            return result

        except IndexError as e:
            msg = f"sql语句执行失败，请检查setup_sql语句是否正确:{sql_list}"
            log_error.logger.error(msg)
            raise ValueError(msg) from e


class ExecutionAssert(HandleMysql):
    """
    处理断言sql数据
    """

    def execution_assert(self, sql: list, res_data: dict) -> dict:
        """
        负责处理yaml文件中的断言需要执行多条 sql 的场景，最终会将所有数据以对象形式返回
        :param sql: 执行的sql语句
        :param res_data: 接口响应数据
        :return:
        """
        try:
            if isinstance(sql, list):
                data = {}
                sql_type = ['UPDATE', 'update', 'DELETE', 'delete', 'INSERT', 'insert']
                if any(i in sql for i in sql_type) is False:
                    for item in sql:
                        sql = sql_regular(item, res_data)
                        if sql:
                            query_data = self.query(sql)[0]
                            data = self.handler_sql_data_type(query_data, data)
                        else:
                            raise ValueError(f"该条sql未查询出任何数据, {sql}")
                else:
                    raise ValueError("断言的 sql 必须是查询的 sql")
            else:
                raise ValueError("sql数据类型不正确，接受的是list")
            return data

        except Exception as e:
            log_error.logger.error("数据库连接失败，失败原因 %s", e)
            raise e

    @classmethod
    def handler_sql_data_type(cls, query_data, data):
        """
        处理部分sql查询的数据格式类型
        :param query_data: 查询出来的sql数据
        :param data: 数据池
        :return:
        """

        for key, value in query_data.items():
            # 1.判断value是否是小数类型
            if isinstance(value, decimal.Decimal):
                data[key] = float(value)
            # 2.判断value是否是时间类型
            elif isinstance(value, datetime.datetime):
                data[key] = str(value)
            else:
                data[key] = value
        return data


if __name__ == '__main__':
    a = HandleMysql()
    b = a.query(sql="select * from `test_obp_configure`.lottery_prize where activity_id = 3")
    print(b)
