#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2022/3/28 12:52
# @Author : liuxw20
"""

import os
import time
import urllib
import uuid
from typing import Dict, Union
import requests
import urllib3
from requests_toolbelt import MultipartEncoder
from utils.handler_cache.set_api_to_cache import SetApiToCache
from utils.handler_cache.update_case_cache import update_case_cache
from utils.handler_conf.conf_control import conf
from utils.handler_enum.depend_data_enum import DependDataEnum
from utils.handler_enum.request_params_enum import RequestParamsEnum
from utils.handler_enum.set_api_cache_enum import SetApiCacheEnum
from utils.handler_other.common import get_expect_result
from utils.handler_path.path_contr import HandlePath
from utils.handler_log.log_control import log_error, log_warning
from utils.handler_log.log_decorator import log_decorator, execution_duration
from utils.handler_mysql.mysql_control import SetupMysql, ExecutionAssert

# from utils.handler_request.encryption_algorithm_control import encryption
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 屏蔽警告信息


class HandleRequest:
    """ 封装请求 """

    @log_decorator(True)
    @execution_duration(3000)
    # @encryption("md5")
    def request(self, case_data: Dict, depend_switch=True):
        """
        http请求封装
        :param case_data: 从yaml文件中读取出来的用例数据
        :param depend_switch: 用例依赖开关, 默认需要依赖
        :param kwargs:
        :return:
        """
        # 1.判断用例状态是否需要执行
        if self.case_is_run(case_data):

            # 2.更新测试数据--目的是提取最新缓存数据
            case_data = eval(update_case_cache(str(case_data)))

            # 3.获取测试数据
            url = case_data[RequestParamsEnum.URL.value]
            method = case_data[RequestParamsEnum.METHOD.value]
            headers = case_data[RequestParamsEnum.HEADERS.value]
            is_token = case_data.get(RequestParamsEnum.IS_TOKEN.value)

            data = case_data[RequestParamsEnum.DATA.value]
            params = case_data[RequestParamsEnum.PARAMS.value]
            json = case_data[RequestParamsEnum.JSON.value]
            files = case_data[RequestParamsEnum.FILES.value]
            export = case_data[RequestParamsEnum.EXPORT.value]

            is_depend = case_data[DependDataEnum.IS_DEPEND.value]
            setup_sql = case_data.get(RequestParamsEnum.SETUP_SQL.value)
            set_api_cache = case_data[SetApiCacheEnum.SET_API_CACHE.value]
            time_sleep = case_data[RequestParamsEnum.SLEEP.value]

            # 4.处理前置sql
            sql_result = SetupMysql().get_setup_sql_data(setup_sql)

            # 5.处理依赖数据逻辑
            if depend_switch is True:
                if is_depend is True:
                    from utils.handler_request.depend_control import HandleDepend
                    HandleDepend().get_depend_data(case_data, sql_result)

            # 6.处理休眠
            if time_sleep is not None:
                time.sleep(time_sleep)

            # 7.获取响应结果
            response = self.send_request(url, method, headers, params, json, data, files, export, is_token)

            # 8.将当前接口的信息写入缓存文件中
            SetApiToCache(set_api_cache, case_data, response).set_main_caches()

            # 9.将请求信息和响应结果集成到一起进行返回
            return self.get_request_result(response, case_data)

    def send_request(self, url, method, headers, params, json, data, files, export, is_token):
        """
        发送不同的请求
        :param url:
        :param method:
        :param headers:
        :param params:
        :param json:
        :param data:
        :param files:
        :param export:
        :return:
        """
        # 同步处理请求头
        headers = self.set_headers(headers, is_token)

        # 1.单独处理上传文件
        if files:
            multipart, files_header = self.upload_file(files, headers)
            headers.update(files_header)
            res = requests.request(url=url, method=method, headers=headers, params=params, data=multipart)

        # 2.单独处理导出文件
        elif export:
            res = requests.request(url=url, method=method, headers=headers, params=params, data=data, json=export)
            self.export_file(res)

        # 3.处理其他请求类型
        else:
            res = requests.request(url=url, method=method, headers=headers, params=params, data=data, json=json)

        return res

    def get_request_result(self, response: object, case_data: dict) -> dict:
        """
        将请求信息和响应信息集成到一起
        :param response: 响应对象
        :param case_data: 测试数据
        :return:
        """
        expect_result=get_expect_result(case_data[RequestParamsEnum.ASSERT.value])
        result_data = {
            "is_run": case_data[RequestParamsEnum.IS_RUN.value],
            "title": case_data[RequestParamsEnum.TITLE.value],

            "url": response.url,
            "method": response.request.method,
            "response_data": response.text,
            "status_code": response.status_code,
            "cookie": response.cookies,
            "headers": response.request.headers,
            'request_body': {},
            "yaml_data": case_data,
            "sql_data": self.handler_sql_data(case_data[RequestParamsEnum.SQL.value], response),
            "assert": case_data[RequestParamsEnum.ASSERT.value],
            "teardown_case": case_data[RequestParamsEnum.TEARDOWN_CASE.value],
            "teardown_sql": case_data[RequestParamsEnum.TEARDOWN_SQL.value],
            "res_time": self.api_response_time(response),
            "expect_result": expect_result
        }

        # 提取请求数据--这个用于日志专用，判断如果是get请求,返回None 直接打印url
        data = case_data.get(RequestParamsEnum.DATA.value)
        params = case_data.get(RequestParamsEnum.PARAMS.value)
        _json = case_data.get(RequestParamsEnum.JSON.value)
        files = case_data.get(RequestParamsEnum.FILES.value)
        export = case_data.get(RequestParamsEnum.EXPORT.value)
        if data:
            result_data['request_body']['data'] = data
        if params:
            result_data['request_body']['params'] = params
        if _json:
            result_data['request_body']['json'] = _json
        if files:
            result_data['request_body']['files'] = files
        if export:
            result_data['request_body']['export'] = export

        return result_data

    @classmethod
    def upload_file(cls, files: dict, data: Union[dict, None], headers: Union[dict, None]) -> tuple:
        """
        处理上传多个文件的情况
        :param files:
        :return:
        """

        file_data = {}
        cls.file_and_data(data, file_data)

        for key, value in files.items():
            if os.path.exists(file_path):
                file_path = HandlePath.FILES_DIR + value
                file_data[key] = (value, open(file_path, 'rb'), 'application/octet-stream')
            else:
                log_error.logger.error("上传的文件路径不存在:{}".format(file_path))
                raise FileNotFoundError("上传的文件路径不存在:{}".format(file_path))

        # 2.解析上传的文件
        multipart = MultipartEncoder(fields=file_data, boundary=uuid.uuid4())

        # 3.重新定义content_type
        if headers is None:
            headers = {}
        headers['Content-Type'] = multipart.content_type

        return multipart, headers

    @classmethod
    def file_and_data(cls, data: dict, file_data: dict) -> None:
        """
        处理上传文件时，携带data表单类型参数
        兼容又要上传文件，又要上传其他类型参数
        """
        if data:
            for key, value in data.items():
                file_data[key] = value

    @classmethod
    def get_export_api_filename(cls, res: object) -> str:
        """
        处理导出文件, 提取文件名
        :param res:
        :return:
        """
        content_disposition = res.headers.get('content-disposition')
        filename_code = content_disposition.split("=")[-1]
        filename = urllib.parse.unquote(filename_code)
        return filename

    @classmethod
    def export_file(cls, res: object) -> None:
        """
        导出文件到本地
        :param res:
        :return:
        """
        file_path = os.path.join(HandlePath.FILES_DIR, cls.get_export_api_filename(res))
        if res.status_code == 200:
            if res.text:
                with open(file_path, 'wb') as fp:
                    for chunk in res.iter_content(chunk_size=1):
                        fp.write(chunk)
            else:
                log_warning.logger.warning('需要导出的文件为空')

    @classmethod
    def case_is_run(cls, case_data) -> bool:
        """
        判断用例是否执行
        :return:
        """
        is_run = case_data[RequestParamsEnum.IS_RUN.value]
        if is_run is True or is_run is None:
            return True

        title = case_data[RequestParamsEnum.TITLE.value]
        log_warning.logger.warning(f'该用例跳过未执行: "{title}" ')
        return False

    @classmethod
    def handler_sql_data(cls, sql_data: list, response: object) -> dict:
        """
        处理 sql参数
        :param sql_data:
        :param response:
        :return:
        """
        if sql_data:
            result = ExecutionAssert().execution_assert(sql_data, response.json())
        else:
            result = {"sql": None}
        return result

    @classmethod
    def api_response_time(cls, response) -> float:
        """
        获取接口响应时长
        """
        try:
            # 保留俩位小数
            return round(response.elapsed.total_seconds() * 1000, 2)
        except AttributeError:
            return 0.00

    def set_headers(self, headers: dict, is_token: Union[bool, None]) -> dict:
        """
        获取用例的请求头
        :param headers:
        :param is_token:
        :return:
        """

        if headers:
            headers.update(self.get_extra_headers(is_token))
        else:
            headers = {}
            headers.update(self.get_extra_headers(is_token))
        return headers

    def get_extra_headers(self, is_token: Union[bool, None]) -> dict:
        """
        获取额外的请求头和token配置
        :param is_token:
        :return:
        """
        _headers = {}
        # 1.获取额外头部
        _headers.update(eval(conf.get('env', 'headers')))
        # 2.处理局部token配置
        if is_token is False:
            return _headers

        # 3.处理全局token配置
        _is_token = conf.getboolean('token', 'is_token')
        if _is_token:
            item = conf.options("token")
            token = {item[2]: conf.get('token', item[2])}
            _headers.update(token)

        return _headers

