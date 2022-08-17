#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/9 16:57
# @Author  : liuxw20
import os
import requests
from ruamel import yaml
from utils.handler_path.path_contr import get_path


class HandlerSwagger:

    def __init__(self, url, headers=None, dir_name1='swagger_data'):
        self.url = url,
        self.headers = headers,
        self.dir_name1 = dir_name1

    def generate_cases(self):
        """
        将解析后的数据写入yaml文件
        :return:
        """
        data = self.get_last_data()
        if data:
            # 1.创建存放解析swagger数据用例的文件夹
            data_dir = get_path(self.dir_name1)
            if not os.path.exists(data_dir):
                os.mkdir(data_dir)

            # 2.解析数据
            for path, item in data.items():
                # 提取2级目录名,和文件名
                dir_name2, *file_name = path.split('/')
                if file_name:
                    filename = ''.join([i for i in file_name])
                else:
                    filename = dir_name2
                filename += '.yaml'

                # 3.创建每个用例文件目录
                dir_name2 = os.path.join(data_dir, dir_name2)
                if not os.path.exists(dir_name2):
                    os.mkdir(dir_name2)

                # 4.写入用例数据
                with open(os.path.join(dir_name2, filename), 'w', encoding='utf-8') as fp:
                    yaml.dump(item, fp, Dumper=yaml.RoundTripDumper, allow_unicode=True)

    def get_last_data(self):
        """
        对基础数据进行二次解析,生成用例模板
        :return:
        """
        data = self.get_base_data()
        if data:
            case_data = {}
            for key, value in data.items():
                case = {}
                for i, attrs in enumerate(value):
                    temp = {
                        'url': key,
                        "method": attrs,
                        "title": value[attrs],
                        "headers": None,
                        f"{'params' if attrs == 'get' else 'data'}": None,
                        "is_run": True,
                        "is_depend": False,
                        "depend_case_data": None,
                        "setup_sql": None,
                        "assert": None,
                    }
                    case.update({f'test_0{i + 1}': temp})
                    new_name = str(key).strip('/')
                case_data.update({new_name: case})
            return case_data

    def get_base_data(self):
        """
        从swagger中解析基础数据
        :param url:
        :return:
        """
        data = self.get_swagger_data()
        if data:
            paths = data['paths']  # 取接口地址返回的path数据，包括请求的路径
            base_data = {}
            for adders, item in paths.items():
                dict1 = {}
                for _method, values in item.items():
                    if isinstance(values, dict):
                        title = values.get('description')
                        dict1[_method] = title
                base_data[adders] = dict1
            return base_data

    def get_swagger_data(self):
        response = requests.get(url=self.url, headers=self.headers).json()
        return response.get('paths')


if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/api/swagger/?format=openapi'
    headers = {
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Imxlbm92byIsImV4cCI6MTY2MDI4NjgxMywiZW1haWwiOiJsZW5vdm9AcXEuY29tIn0.CS6Vf9e5ZqeUn7TyO8XsY_qGp1APGhqXhwcCKXKQ6E8'
    }
    HandlerSwagger(url,headers=None).generate_cases()

