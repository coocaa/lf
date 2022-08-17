#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 12:34
# @Author  : liuxw20
import time
import pytest
from utils.handler_other.handle_login import HandleLogin
from utils.handler_log.log_control import log_info


@pytest.fixture(scope="session", autouse=True)
def init_login():
    """
    处理登录的token,和cookie逻辑
    :return:
    """
    HandleLogin().handle_login()


@pytest.fixture(scope="function", autouse=True)
def case_skip(case_item):
    """
    处理跳过用例
    :param case_item:
    :return:
    """
    if case_item['is_run'] is False:
        pytest.skip()


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的 item 的 name 和 node_id 的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")  # 用例方法名
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")  # 用例节点位置

    # 1.指定运行顺序用例
    case_func_names = ["test_REGISTER", "test_LOGIN", "test_Cart_List", "test_ADD", "test_Guest_ADD",
                       "test_Clear_Cart_Item"]

    # 2.提取指定顺序的用例
    last_run_items = []
    for case in case_func_names:
        for item in items:
            func_name = item.name.split("[")[0]
            if case == func_name:
                last_run_items.append(item)

    # 3.将指定的运行的用例顺序与原先的进行交换
    for run_item in last_run_items:
        # 1.获取指定运行用例顺序的下标
        last_index = last_run_items.index(run_item)
        # 2.获取原先运行用例顺序的下标
        old_index = items.index(run_item)

        if old_index != last_index:
            last_case = items[last_index]
            old_index = items.index(last_case)
            # 3.将用例执行顺序进行替换
            items[last_index], items[old_index] = items[old_index], items[last_index]


def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    """
    _total = terminalreporter._numcollected
    _pass = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _times = time.time() - terminalreporter._sessionstarttime

    log_info.logger.info(f"用例总数: {_total}")
    log_info.logger.info(f"通过用例数: {_pass}")
    log_info.logger.error(f"异常用例数: {_error}")
    log_info.logger.error(f"失败用例数: {_failed}")
    log_info.logger.warning(f"跳过用例数: {_skipped}")
    log_info.logger.info("用例执行时长: %.2f" % _times + " s")

    try:
        rate = _pass / _total * 100
        log_info.logger.info("用例成功率: %.2f" % rate + " %")
    except ZeroDivisionError:
        log_info.logger.info("用例成功率: 0.00 %")
