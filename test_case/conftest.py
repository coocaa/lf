#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 12:34
# @Author  : liuxw20
import time
import pytest
from utils.handler_other.handle_login import HandleLogin
from utils.handler_path.path_contr import HandlePath
from utils.handler_cache.cache_control import HandleCache
from utils.handler_other.common import get_case_files
from utils.handler_yaml.yaml_analysis import AnalysisYamlData
from utils.handler_log.log_control import log_error, log_info


@pytest.fixture(scope="session", autouse=True)
def init_login():
    """
    处理登录的token,和cookie逻辑
    :return:
    """
    HandleLogin().handle_login()


@pytest.fixture(scope="session", autouse=True)
def set_cases_cache():
    """
    获取所有用例，写入缓存文件
    :return:
    """

    cache_data = {}

    for file_path in get_case_files(data_dir=HandlePath.DATA_DIR):
        case_list = AnalysisYamlData(file_path).analysis(case_id_mark=True)
        for case in case_list:
            for key, value in case.items():  # key==case_id

                if key in cache_data.keys():
                    log_error.logger.error(f"case_id: {key} 重复了, 请修改case_id\n"
                                           f"文件路径: {file_path}")
                    raise ValueError(f"case_id: {key} 重复了, 请修改case_id\n"
                                     f"文件路径: {file_path}")
                else:

                    cache_data[key] = value

    # 将所有的测试用例写入缓存文件中
    HandleCache(filename='cases_cache.json').set_json_cache(cache_data)


@pytest.fixture(scope="function", autouse=True)
def case_skip(case_item):
    """处理跳过用例"""
    if case_item['is_run'] is False:
        pytest.skip()


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的 item 的 name 和 node_id 的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    """
    _total = terminalreporter._numcollected
    _pass = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _times = time.time() - terminalreporter._sessionstarttime

    log_info.logger.info(f"用例总数: {_total}")
    log_info.logger.info(f"通过用例数: {_pass}")
    log_info.logger.error(f"异常用例数: {_error}")
    log_info.logger.error(f"失败用例数: {_failed}")
    log_info.logger.warning(f"跳过用例数: {skipped}")
    log_info.logger.info("用例执行时长: %.2f" % _times + " s")

    try:
        rate = _pass / _total * 100
        log_info.logger.info("用例成功率: %.2f" % rate + " %")
    except ZeroDivisionError:
        log_info.logger.info("用例成功率: 0.00 %")
