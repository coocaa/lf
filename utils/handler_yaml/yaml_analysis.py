#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022-08-01 10:57:25
# @Author : liuxw20
from typing import Union

from utils.handler_conf.conf_control import conf
from utils.handler_path.path_contr import HandlePath
from utils.handler_enum.depend_data_enum import DependDataEnum
from utils.handler_enum.request_params_enum import RequestParamsEnum
from utils.handler_yaml.yaml_control import HandleYaml
from utils.handler_conf.get_conf_data import db_status
from utils.handler_log.log_control import log_error


class AnalysisYamlData:
    """
    yaml 数据解析, 判断数据填写是否符合规范,并提取测试数据
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def analysis(self, case_id_mark: bool = False) -> list:
        """
        yaml文件数据解析,返回该 yaml文件中的所有用例
        :param case_id_mark: 判断解析是否需要提取出 case_id, 主要用于兼容用例,缓存文件中的数据
        :return:
        """
        yaml_data = HandleYaml.read_yaml(self.file_path)

        case_list = []
        for key, value in yaml_data.items():  # key是用例的id
            case_data = {

                RequestParamsEnum.TITLE.value: self.check_title(key, value),
                RequestParamsEnum.URL.value: self.check_url(key, value),
                RequestParamsEnum.METHOD.value: self.check_method(key, value),
                RequestParamsEnum.HEADERS.value: self.check_headers(key, value),
                RequestParamsEnum.IS_RUN.value: self.check_is_run(key, value),
                RequestParamsEnum.IS_TOKEN.value: self.check_is_token(value),
                RequestParamsEnum.DATA.value: self.check_data(key, value),
                RequestParamsEnum.PARAMS.value: self.check_params(key, value),
                RequestParamsEnum.JSON.value: self.check_json(key, value),
                RequestParamsEnum.FILES.value: self.check_file(key, value),
                RequestParamsEnum.EXPORT.value: self.check_export(key, value),

                DependDataEnum.IS_DEPEND.value: self.check_is_depend(key, value),
                DependDataEnum.DEPEND_CASE_DATA.value: self.check_depend_case_data(key, value),
                RequestParamsEnum.ASSERT.value: self.check_assert(key, value),
                RequestParamsEnum.SQL.value: self.check_sql(key, value),
                RequestParamsEnum.SETUP_SQL.value: self.setup_sql(value),
                RequestParamsEnum.TEARDOWN_SQL.value: self.teardown_sql(value),
                RequestParamsEnum.TEARDOWN_CASE.value: self.teardown_case(value),
                RequestParamsEnum.SLEEP.value: self.time_sleep(value),
                RequestParamsEnum.SET_API_CACHE.value: self.set_api_cache(value)
            }

            if case_id_mark is True:
                case_list.append({key: case_data})
            else:
                case_list.append(case_data)

        return case_list

    def check_is_run(self, case_id: str, case_data: dict) -> bool:
        """
        获取执行状态,True或者None都会执行
        :param case_id:
        :param case_data:
        :return:
        """
        try:
            return case_data[RequestParamsEnum.IS_RUN.value]
        except KeyError as e:
            raise KeyError(self.raise_key_null(case_id, key=RequestParamsEnum.IS_RUN.value)) from e

    def check_title(self, case_id: str, case_data: dict) -> str:
        """
        获取用例标题
        :param case_id:
        :param case_data:
        :return:
        """
        try:
            return case_data[RequestParamsEnum.TITLE.value]
        except KeyError as e:
            raise KeyError(self.raise_key_null(case_id, key=RequestParamsEnum.TITLE.value)) from e

    def check_method(self, case_id: str, case_data: dict) -> str:
        """
        获取用例请求方式: GET/POST/PUT/DELETE
        :param case_id:
        :param case_data:
        :return:
        """

        _method = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTION']
        try:
            case_method = case_data[RequestParamsEnum.METHOD.value]
        except KeyError as e:
            raise KeyError(self.raise_key_null(case_id, key=RequestParamsEnum.METHOD.value)) from e

        if case_method.upper() not in _method:
            raise ValueError(
                f"method目前只支持: {_method} 中的请求方式，如需新增请联系liuxw20"
                f"{self.raise_value_error(error_info='请求方式', case_id=case_id, value=case_method)}")
        return case_method.upper()

    def check_url(self, case_id: str, case_data: dict) -> str:
        """
        获取用例的url地址
        :param case_id:
        :param case_data:
        :return:
        """
        try:
            url = case_data[RequestParamsEnum.URL.value]
            if url is None:
                raise ValueError(
                    f"用例中的: url不能为空！\n "
                    f"用例ID: {case_id} \n "
                    f"用例路径: {self.file_path}")

            host = conf.get('env', 'host')
            return host + url

        except KeyError as e:
            raise KeyError(self.raise_key_null(case_id, key=RequestParamsEnum.URL.value)) from e

    def check_headers(self, case_id: str, case_data: dict) -> dict:
        """
        获取用例的请求头
        :param case_id:
        :param case_data:
        :return:
        """
        try:
            headers = case_data[RequestParamsEnum.HEADERS.value]
            if headers:
                headers.update(self.get_extra_headers(case_data))
            else:
                headers = {}
                headers.update(self.get_extra_headers(case_data))
            return headers
        except KeyError as e:
            raise KeyError(self.raise_key_null(case_id, key=RequestParamsEnum.HEADERS.value)) from e

    def check_is_token(self,case_data: dict) -> dict:
        """
        获取用例的token
        :param case_id:
        :param case_data:
        :return:
        """

        is_token = case_data.get(RequestParamsEnum.IS_TOKEN.value)

        if is_token is False:
            return False
        return True

    def check_data(self, case_id: str, case_data: dict) -> Union[dict, None]:
        """
        获取用例的表单类型数据
        :param case_id:
        :param case_data:
        :return:
        """
        return case_data.get(RequestParamsEnum.DATA.value)

    def check_params(self, case_id: str, case_data: dict) -> Union[dict, None]:
        """
        获取用例的路径类型数据
        :param case_id:
        :param case_data:
        :return:
        """

        return case_data.get(RequestParamsEnum.PARAMS.value)

    def check_json(self, case_id: str, case_data: dict) -> Union[dict, None]:
        """
        获取用例的json类型数据
        :param case_id:
        :param case_data:
        :return:
        """
        return case_data.get(RequestParamsEnum.JSON.value)

    def check_file(self, case_id: str, case_data: dict) -> Union[dict, None]:
        """
        获取用例的文件类型数据
        :param case_id:
        :param case_data:
        :return:
        """
        return case_data.get(RequestParamsEnum.FILES.value)

    def check_export(self, case_id: str, case_data: dict) -> Union[dict, None]:
        """
        获取用例的导出文件类型数据
        :param case_id:
        :param case_data:
        :return:
        """
        return case_data.get(RequestParamsEnum.EXPORT.value)

    def check_is_depend(self, case_id: str, case_data: dict) -> bool:
        """
        获取用例的依赖状态
        :param case_id:
        :param case_data:
        :return:
        """
        try:
            return case_data[DependDataEnum.IS_DEPEND.value]
        except KeyError as e:
            raise KeyError(self.raise_key_null(case_id, key=DependDataEnum.IS_DEPEND.value)) from e

    def check_depend_case_data(self, case_id: str, case_data: dict) -> dict:
        """
        获取用例的依赖数据
        :param case_id:
        :param case_data:
        :return:
        """
        # 判断如果该用例有依赖，则返回依赖数据，否则返回None
        if self.check_is_depend(case_id, case_data) is True:
            try:
                depend_case_data = case_data[DependDataEnum.DEPEND_CASE_DATA.value]
                # 判断当用例中设置的需要依赖用例，但是dependence_data下方没有填写依赖的数据，异常提示
                if depend_case_data is None:
                    raise ValueError(f"depend_case_data 依赖数据中缺少依赖相关数据！"
                                     f"如有填写，请检查缩进是否正确"
                                     f"用例ID: {case_id}"
                                     f"用例路径: {self.file_path}")
                return depend_case_data

            except KeyError as e:
                raise KeyError(self.raise_key_null(case_id, key=DependDataEnum.DEPEND_CASE_DATA.value)) from e
        else:
            return {DependDataEnum.DEPEND_CASE_DATA.value: None}

    def check_assert(self, case_id: str, case_data: dict) -> Union[dict, None]:
        """
        获取用例的断言数据
        :param case_id:
        :param case_data:
        :return:
        """
        try:
            return case_data[RequestParamsEnum.ASSERT.value]
        except KeyError as e:
            raise KeyError(self.raise_key_null(case_id, key=RequestParamsEnum.ASSERT.value)) from e

    def check_sql(self, case_id: str, case_data: dict) -> Union[list, None]:
        """
        获取用例的断言sql
        :param case_id:
        :param case_data:
        :return:
        """
        try:
            # 判断数据库是否开启
            if db_status():
                return case_data[RequestParamsEnum.SQL.value]
            return None

        except KeyError as e:
            raise KeyError(self.raise_key_null(case_id, key=RequestParamsEnum.SQL.value)) from e

    @classmethod
    def setup_sql(cls, case_data: dict) -> Union[list, None]:
        """
        获取前置sql，比如该条用例中需要从数据库中读取sql作为用例参数,没有返回None
        :return:
        """
        return case_data.get(RequestParamsEnum.SETUP_SQL.value)

    @classmethod
    def teardown_sql(cls, case_data: dict) -> Union[list, None]:
        """
        获取后置sql，比如该条用例中需要从数据库中读取sql作为用例参数,没有返回None
        :return:
        """
        return case_data.get(RequestParamsEnum.TEARDOWN_SQL.value)

    @classmethod
    def teardown_case(cls, case_data: dict) -> Union[dict, None]:
        """
        获取后置请求数据,没有返回None
        :return:
        """

        return case_data.get(RequestParamsEnum.TEARDOWN_CASE.value)

    @classmethod
    def time_sleep(cls, case_data: dict) -> Union[str, None]:
        """
        设置休眠时间, 没有返回None
        :return:
        """
        return case_data.get(RequestParamsEnum.SLEEP.value)

    @classmethod
    def set_api_cache(cls, case_data: dict) -> Union[dict, None]:
        """
        将当前请求的用例测试数据存入缓存
        :return:
        """

        return case_data.get(RequestParamsEnum.SET_API_CACHE.value)

    def get_extra_headers(self,case_data) -> dict:
        """
        获取额外的请求头和token配置
        :param case_data:
        :return:
        """
        _headers = {}
        # 获取额外头部
        _headers.update(eval(conf.get('env', 'headers')))
        if self.check_is_token(case_data) is False:
            return _headers

        is_token = conf.getboolean('token', 'is_token')
        if is_token:
            item = conf.options("token")
            token = {item[2]: conf.get('token', item[2])}
            _headers.update(token)
        return _headers

    def raise_key_null(self, case_id, key) -> str:
        """
        抛出测试用例参数名key不存在的异常信息
        :param case_id: 用例id
        :param key: 参数名
        :return:
        """
        detail = f'用例中未找到: "{key}" 参数， 如已填写，请检查用例缩进是否存在问题' \
                 f"用例ID: {case_id}\n " \
                 f"用例路径: {self.file_path}"
        log_error.logger.error(detail)
        return detail

    def raise_value_error(self, error_info, case_id, value) -> str:
        """
        所有的用例填写不规范的异常提示
        :param error_info: 错误信息
        :param case_id: 用例ID
        :param value: 参数值
        :return:
        """
        detail = f"用例中的 {error_info} 填写不正确！\n " \
                 f"用例ID: {case_id} \n" \
                 f"用例路径: {self.file_path}\n" \
                 f"当前填写的value: {value}"

        log_error.logger.error(detail)
        return detail


if __name__ == '__main__':
    result = AnalysisYamlData(HandlePath.DATA_DIR + 'Login/login.yaml').analysis()
    print(result)
