#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/28 15:21
# @Author : liuxw20

from functools import wraps
from utils.handler_log.log_control import log_error, log_info


def log_decorator(switch: bool):
    """
    封装日志装饰器, 打印请求信息 默认为 True
    :param switch: 定义日志开关
    :return:
    """
    def decorator(func):
        @wraps(func)
        def swapper(*args, **kwargs):
            res = func(*args, **kwargs)
            # 判断日志开关为开启状态
            if switch:
                _log_msg = f"\n===========================================================\n" \
                               f"用例标题: {res['title']}\n" \
                               f"请求路径: {res['url']}\n" \
                               f"请求方式: {res['method']}\n" \
                               f"请求头:   {res['headers']}\n" \
                               f"请求内容: {res['request_body']}\n" \
                               f"响应内容: {res['response_data']}\n" \
                               f"预期结果: {res['expect_result']}\n" \
                               f"接口响应时长: {res['res_time']} ms\n" \
                               f"Http状态码: {res['status_code']}\n" \
                               "=========================================================="
                _is_run = res['is_run']
                # 判断正常打印的日志，控制台输出绿色
                if _is_run in (True, None) and res['status_code'] == 200:
                    log_info.logger.info(_log_msg)
                else:
                    # 失败的用例，控制台打印红色
                    log_error.logger.error(_log_msg)
            return res
        return swapper
    return decorator


def execution_duration(number: int):
    """
    统计请求运行时长装饰器，如请求响应时间超时
    程序中会输入红色日志，提示时间 http 请求超时，默认时长为 3000ms
    :param number: 函数预计运行时长
    :return:
    """

    def decorator(func):
        def swapper(*args, **kwargs):
            res= func(*args, **kwargs)
            run_time = res['res_time']
            # 计算时间戳毫米级别，如果时间大于number，则打印 函数名称 和运行时间
            if run_time > number:
                log_info.logger.warning(
                    "\n==============================================\n"
                    "测试用例执行时间较长，请关注.\n"
                    "函数运行时间: %s ms\n"
                    "测试用例相关数据: %s\n"
                    "================================================="
                    , run_time, res)
            return res
        return swapper
    return decorator