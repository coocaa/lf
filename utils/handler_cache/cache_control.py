#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/28 15:28
# @Author : liuxw20

cases_cache = {}

depend_cache = {}


class HandleCache:
    """
    缓存操作: 设置,读取
    """

    @staticmethod
    def set_cases_cache(case_id, values):
        """
        设置所有用例缓存
        :param case_id:
        :param values:
        :return:
        """
        cases_cache[case_id] = values

    @staticmethod
    def get_cases_cache(case_id):
        """
        获取单个用例缓存
        :param case_id:
        :return:
        """
        return cases_cache.get(case_id)

    @staticmethod
    def set_cache(case_name, value):
        """
        设置单个依赖缓存
        :param case_name:
        :param value:
        :return:
        """
        depend_cache[case_name] = value

    @staticmethod
    def get_cache(case_name):
        """
        获取单个依赖缓存
        :param case_name:
        :return:
        """
        return depend_cache.get(case_name)

    @classmethod
    def get_case_data(cls, case_ids):
        """
        根据id获取所有测试用例数据
        :param case_ids:
        :return:
        """
        case_data_list = []
        for id in case_ids:
            case_data = cls.get_cases_cache(id)
            case_data_list.append(case_data)

        return case_data_list
