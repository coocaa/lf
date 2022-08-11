#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022-08-10 20:12:50
# @Author : liuxw20
import pytest
from utils.handler_path.path_contr import HandlePath
from utils.handler_assert.assert_control import HandleAssert
from utils.handler_yaml.yaml_analysis import AnalysisYamlData
from utils.handler_request.request_control import HandleRequest
from utils.handler_request.teardown_control import HandlerTeardown

TestData = AnalysisYamlData(HandlePath.DATA_DIR + r'Recharge/recharge.yaml').analysis()


class TestRecharge:


    @pytest.mark.parametrize('case_item', TestData)
    def test_recharge(self, case_item):
        """
        :param :
        :return:
        """

        res_info = HandleRequest().request(case_item)
        HandlerTeardown().handle_teardown(res_info)
        HandleAssert(case_item).handle_assert(res_info)



if __name__ == '__main__':
    pytest.main(['test_recharge.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
