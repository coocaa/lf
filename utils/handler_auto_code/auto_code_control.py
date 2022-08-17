#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/8/8 15:28
# @Author : liuxw20
import os

from utils.handler_path.path_contr import HandlePath
from utils.handler_auto_code.case_template import write_testcase_file
from utils.handler_other.common import get_os_sep, get_case_files
from utils.handler_yaml.yaml_control import HandleYaml


class AutomaticGenerationTestCase:
    """
    处理自动生成自动化测试中的test_case代码
    """

    def automatic_code(self) -> None:
        """
        自动生成 测试代码逻辑处理
        :return:
        """
        file_path_list = get_case_files(data_dir=HandlePath.DATA_DIR, filter_yaml=True)

        for file_path in file_path_list:
            if 'proxy_data.yaml' not in file_path:
                # 生成test_case路径
                self.mk_dir(file_path)
                case_data = HandleYaml.read_yaml(file_path)
                # 提取至模板中
                write_testcase_file(
                    class_name=self.get_test_class_name(file_path),
                    func_name=self.get_test_func_name(file_path),
                    case_ids=self.get_case_ids(case_data),
                    case_path=self.get_case_path(file_path)[0],
                    file_name=self.get_case_path(file_path)[1])

    def mk_dir(self, file_path: str) -> None:
        """
        判断生成自动化代码的文件夹路径是否存在，如果不存在，则自动创建
        :param file_path:
        :return:
        """
        _case_dir_path = os.path.split(self.get_case_path(file_path)[0])[0]
        if not os.path.exists(_case_dir_path):
            os.makedirs(_case_dir_path)

    def get_case_path(self, file_path: str) -> tuple:
        """
        根据yaml中的用例,生成对应 testCase 层代码的路径
        :param file_path: yaml用例路径
        :return: D:\\Project\\test_case\\test_case_demo.py, test_case_demo.py
        """

        # 这里通过“\\” 符号进行分割，提取出来文件名称
        path = self.get_file_name(file_path).split(get_os_sep())
        # 判断生成的 testcase 文件名称，需要以test_ 开头
        case_name = path[-1] = path[-1].replace(path[-1], "test_" + path[-1])
        new_name = get_os_sep().join(path)
        return HandlePath.CASE_DIR + new_name, case_name

    def get_file_name(self, file_path: str) -> str:
        """
        通过 yaml文件的命名，将名称转换成 py文件的名称
        :param file_path: yaml 文件路径
        :return:  示例： DateDemo.py
        """
        # 1.提取"data_dir"目录的路径长度
        num = len(HandlePath.DATA_DIR)
        yaml_path = file_path[num:]
        file_name = None
        # 路径转换
        if '.yaml' in yaml_path:
            file_name = yaml_path.replace('.yaml', '.py')
        elif '.yml' in yaml_path:
            file_name = yaml_path.replace('.yml', '.py')
        return file_name

    def get_test_class_name(self, file_path: str) -> str:
        """
        自动生成类名称
        :param file_path:
        :return: sup_apply_list --> SupApplyList
        """
        # 提取文件名称
        _file_name = os.path.split(self.get_file_name(file_path))[1][:-3]
        _name = _file_name.split("_")
        _name_len = len(_name)
        # 将文件名称格式，转换成类名称: sup_apply_list --> SupApplyList
        for i in range(_name_len):
            _name[i] = _name[i].capitalize()
        _class_name = "".join(_name)

        return _class_name

    def get_test_func_name(self, file_path: str) -> str:
        """
        函数名称
        :param file_path: yaml 用例路径
        :return:
        """

        _file_name = os.path.split(self.get_file_name(file_path))[1][:-3]
        return _file_name

    def get_case_ids(self, case_data):
        """
        获取所有的用例 ID
        :param case_data:
        :return:
        """
        return [key for key in case_data.keys()]



    @classmethod
    def error_message(cls, param_name, file_path):
        """
        用例中填写不正确的相关提示
        :return:
        """
        msg = f"用例中未找到 {param_name} 参数值，请检查新增的用例中是否填写对应的参数内容" \
              "如已填写，可能是 yaml 参数缩进不正确\n" \
              f"用例路径: {file_path}"
        return msg


if __name__ == '__main__':
    AutomaticGenerationTestCase().automatic_code()
