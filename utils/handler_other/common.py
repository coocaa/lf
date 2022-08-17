#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/8 14:50
# @Author  : liuxw20
import os
import types
import socket
from typing import Dict, Callable



def get_case_files(data_dir, filter_yaml=True) -> list:
    """
    获取所有测试数据的文件路径
    :param data_dir: 测试数据目录
    :param filter_yaml: 是否过滤文件为 yaml格式， True则过滤
    :return:
    """
    filenames = []

    # 获取data目录下的子文件
    for base, dirs, files in os.walk(data_dir):
        for file_path in files:
            last_path = os.path.join(base, file_path)
            if filter_yaml:
                if str(last_path).split('.')[1] in ['yaml', 'yml']:
                    filenames.append(last_path)
            else:
                filenames.append(last_path)
    return filenames


def get_os_sep():
    """
    判断不同的操作系统的路径
    :return: windows 返回 "\", linux 返回 "/"
    """
    return os.sep


def load_module_func(module) -> Dict[str, Callable]:
    """
    获取 module中方法的名称和所在的内存地址
    """
    funcs = {}
    # 函数名和地址
    for name, address in vars(module).items():
        if isinstance(address, types.FunctionType):
            funcs[name] = address
    return funcs




def delete_file(path):
    """删除目录下的文件"""
    list_path = os.listdir(path)
    for item in list_path:
        c_path = os.path.join(path, item)
        if os.path.isdir(c_path):
            delete_file(c_path)
        else:
            os.remove(c_path)


def get_expect_result(assert_data:dict):
    """
    提取预期结果和断言方式
    :param assert_data:
    :return:
    """
    expect_result={}
    if assert_data:
        i=0
        # 遍历第一层
        for name,item in assert_data.items():
            data = {}
            i += 1
            # 遍历第二层
            for key, value in item.items():
                if key == 'assert_type':
                    data[value] = key
                else:
                    if key == 'jsonpath':
                        data[item.get('assert_type')] = value
                    else:
                        data[key] = value

            expect_result['断言'+str(i)] = data

    return expect_result

def get_report_html():
    """
    获取本地的html文件路径
    :return:
    """
    _s = None
    try:
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.connect(('8.8.8.8', 80))
        l_host = _s.getsockname()[0]
    finally:
        _s.close()

    return l_host