#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 15:36
# @Author  : liuxw20
import inspect
import os
import jinja2
import yaml
from jinja2 import UndefinedError
from utils.handler_random import random_control
from utils.handler_path.path_contr import HandlePath
from utils.handler_log.log_control import log_error


class HandleYaml:

    @classmethod
    def get_random_funcs(cls) -> dict:
        """
        提取所有模块的所有函数地址
        :return:
        """
        funcs_address = inspect.getmembers(random_control, inspect.isfunction)

        return dict(funcs_address)

    @classmethod
    def render_yaml(cls, file_path: str) -> str:
        """
        渲染yaml文件
        :param file_path:
        :return:
        """
        path, filename = os.path.split(file_path)
        temp_obj = jinja2.Environment(loader=jinja2.FileSystemLoader(path)).get_template(filename)
        return temp_obj.render(**cls.get_random_funcs())

    @classmethod
    def read_yaml(cls, file_path: str) -> dict:
        """
        获取 yaml 中的数据
        :param: fileDir:
        :return:
        """
        if os.path.exists(file_path):
            try:
                data = cls.render_yaml(file_path)
                return yaml.safe_load(data)
            except UndefinedError as e:
                msg = f'\n读取yaml文件数据失败, 文件路径为:{file_path}, 异常原因: 存在未定义的变量'
                log_error.logger.error(msg)
                raise ValueError(msg)
            except Exception as e:
                msg = "\n请检查相关数据是否填写, 如已填写, 请检查缩进问题"
                log_error.logger.error(msg)
                raise TypeError(msg) from e
        else:
            raise FileNotFoundError("文件路径不存在:{}".format(file_path))


if __name__ == '__main__':
    result = HandleYaml.read_yaml(HandlePath.DATA_DIR + 'Login/login.yaml')
    print(result)
