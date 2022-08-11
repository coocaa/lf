#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2022/3/28 12:52
# @Author : liuxw20
"""
import pytest
from utils.handler_auto_code.auto_code_control import AutomaticGenerationTestCase
from utils.handler_conf.conf_control import conf
from utils.handler_path.path_contr import HandlePath
from utils.handler_inform.send_inform import send_inform
from utils.handler_other.common import delete_file


def cmd():
    # 1.清空所有缓存文件
    delete_file(HandlePath.CACHE_DIR)

    # 2.处理未生成代码的测试用例如
    AutomaticGenerationTestCase().automatic_code()

    # 3.执行程序
    pytest.main(['-s', '-W','ignore:Module already imported:pytest.PytestWarning',
        '--report=report.html',
        f'--title={conf.get("other", "projectName")}测试报告',
        f'--tester={conf.get("other", "author")}',
        '--desc=报告描述信息',
        '--template=2'
        ])

    """
    --reruns: 失败重跑次数
    --count: 重复执行次数
    -v: 显示错误位置以及错误的详细信息
    -s: 等价于 pytest --capture=no 可以捕获print函数的输出
    -q: 简化输出信息
    -m: 运行指定标签的测试用例
    -x: 一旦错误，则停止运行
    --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
    "--reruns=3", "--reruns-delay=2"
    """

    # 4.发送测试报告通知
    # send_inform()


if __name__ == '__main__':
    cmd()
