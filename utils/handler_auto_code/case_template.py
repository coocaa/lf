#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/8/8 15:28
# @Author : liuxw20
import os
import datetime
from utils.handler_conf.conf_control import conf


def write_case(case_path, page):
    """
    写入用例代码
    :param case_path:
    :param page:
    :return:
    """
    with open(case_path, 'w', encoding="utf-8") as file:
        file.write(page)


def write_testcase_file(class_title, func_title, case_path, yaml_path, file_name):
    """
    生成用例模板代码
    :param allure_story:
    :param file_name: 文件名称
    :param allure_epic: 项目名称
    :param allure_feature: 模块名称
    :param class_title: 类名称
    :param func_title: 函数名称
    :param case_path: case 路径
    :param yaml_path: yaml 文件路径
    :return:
    """
    author = conf.get('other', 'author')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_case_status = conf.getboolean('other', 'update_case')

    page = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : {now}
# @Author : {author}
import pytest
from utils.handler_path.path_contr import HandlePath
from utils.handler_assert.assert_control import HandleAssert
from utils.handler_yaml.yaml_analysis import AnalysisYamlData
from utils.handler_request.request_control import HandleRequest
from utils.handler_request.teardown_control import HandlerTeardown

TestData = AnalysisYamlData(HandlePath.DATA_DIR + r'{yaml_path}').analysis()


class Test{class_title}:


    @pytest.mark.parametrize('case_item', TestData)
    def test_{func_title}(self, case_item):
        """
        :param :
        :return:
        """

        res_info = HandleRequest().request(case_item)
        HandlerTeardown().handle_teardown(res_info)
        HandleAssert(case_item).handle_assert(res_info)



if __name__ == '__main__':
    pytest.main(['{file_name}', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
'''

    if update_case_status:
        write_case(case_path=case_path, page=page)
    elif update_case_status is False:
        if not os.path.exists(case_path):
            write_case(case_path=case_path, page=page)
    else:
        raise ValueError("配置文件中的:update_case配置不正确,只能配置 True 或者 False")
