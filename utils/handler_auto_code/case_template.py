#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/8/8 15:28
# @Author : liuxw20
import os
import datetime
from utils.handler_conf.conf_control import conf


def write_case(case_path, code_page):
    """
    写入用例代码
    :param case_path:
    :param page:
    :return:
    """
    with open(case_path, 'w', encoding="utf-8") as file:
        file.write(code_page)


def write_testcase_file(class_name, func_name, case_ids, case_path, file_name):
    """
    :param class_name: 类名
    :param func_name: 函数名
    :param case_ids: 测试用例id
    :param case_path: case 路径
    :param file_name: 代码文件名
    :return:
    """

    author = conf.get('other', 'author')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_case_status = conf.getboolean('other', 'update_case')

    code_page = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : {now}
# @Author : {author}
import pytest
from utils.handler_cache.cache_control import HandleCache
from utils.handler_assert.assert_control import HandleAssert
from utils.handler_request.request_control import HandleRequest
from utils.handler_request.teardown_control import HandlerTeardown


case_ids = {case_ids}
TestData = HandleCache.get_case_data(case_ids)

class Test{class_name}:


    @pytest.mark.parametrize('case_item', TestData)
    def test_{func_name}(self, case_item):
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
        write_case(case_path=case_path, code_page=code_page)
    elif update_case_status is False:
        if not os.path.exists(case_path):
            write_case(case_path=case_path, code_page=code_page)
    else:
        raise ValueError("配置文件中的:update_case配置不正确,只能配置 True 或者 False")
