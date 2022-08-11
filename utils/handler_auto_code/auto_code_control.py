#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/8/8 15:28
# @Author : liuxw20
import os

from utils.handler_path.path_contr import HandlePath
from utils.handler_auto_code.case_template import write_testcase_file
from utils.handler_other.common import get_os_sep, get_case_files


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
                self.mk_dir(file_path)
                write_testcase_file(
                    class_title=self.get_test_class_title(file_path),
                    func_title=self.func_title(file_path),
                    case_path=self.get_case_path(file_path)[0],
                    yaml_path=self.yaml_path(file_path),
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

        num = len(HandlePath.DATA_DIR)
        yaml_path = file_path[num:]
        file_name = None
        if '.yaml' in yaml_path:
            file_name = yaml_path.replace('.yaml', '.py')
        elif '.yml' in yaml_path:
            file_name = yaml_path.replace('.yml', '.py')
        return file_name

    def get_test_class_title(self, file_path: str) -> str:
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

    def func_title(self, file_path: str) -> str:
        """
        函数名称
        :param file_path: yaml 用例路径
        :return:
        """

        _file_name = os.path.split(self.get_file_name(file_path))[1][:-3]
        return _file_name

    def yaml_path(self, file_path: str) -> str:
        """
        生成动态 yaml 路径, 主要处理业务分层场景
        :param file_path: 如业务有多个层级, 则获取到每一层/test_demo/DateDemo.py
        :return: Login/common.yaml
        """
        i = len(HandlePath.DATA_DIR)

        # 兼容 linux 和 window 操作路径
        yaml_path = file_path[i:].replace("\\", "/")

        return yaml_path

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

