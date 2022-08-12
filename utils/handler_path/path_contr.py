#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 10:34
# @Author  : liuxw20
import os
from utils.handler_time.time_control import now_date


def replace_path(path):
    """
    解决路径在win或linux上不兼容的问题-windows 返回 "\", linux 返回 "/"
    :param path: 路径
    :return: 替换后的路径
    """
    path = path.replace('$', os.sep)
    return path


def get_path(dir_name):
    """
    对各模块的路径进行拼接
    :param dir_name: 目录名
    :return: 拼接后的路径
    """
    # 项目的根目录--绝对路径
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(BASE_PATH, dir_name.replace('$', os.sep))


def generate_log_path(filename):
    """
    处理日志文件路径
    """
    log_dir = get_path(f'logs${now_date()}')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    return os.path.join(log_dir, filename)




class HandlePath:
    # 1.测试用例路径
    CASE_DIR = get_path('test_case$')
    # 2.测试数据路径
    DATA_DIR = get_path('data$')
    # 3.日志模块路径
    LOG_DIR = get_path('logs$')
    # 4.配置文件路径
    CONF_PATH = get_path('conf$config.ini')
    # 5.缓存文件路径
    CACHE_DIR = get_path('cache$')
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    # 6.测试上传文件路径
    FILES_DIR = get_path('files$')

    # 7.测试报告路径
    REPORT_DIR = get_path('reports$')

    # 8.日志文件路径
    log_info_path = generate_log_path(f'{now_date()}--info.log')
    log_error_path = generate_log_path(f'{now_date()}--error.log')
    log_warning_path = generate_log_path(f'{now_date()}--warning.log')
