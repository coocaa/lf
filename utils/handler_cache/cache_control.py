#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/28 15:28
# @Author : liuxw20
import json
import os
from typing import Any, Union
from utils.handler_path.path_contr import HandlePath


class HandleCache:
    """
    缓存操作: 设置,读取,删除
    """

    def __init__(self, filename: Union[str, None]) -> None:
        # 如果filename存在，则操作指定文件内容
        if filename:
            self.path = HandlePath.CACHE_DIR + filename
        # 如果filename为None，则操作所有文件内容
        else:
            self.path = HandlePath.CACHE_DIR


    def set_json_cache(self, value: Any) -> None:
        """
        设置多个字典缓存数据, 如果内容存在,则替换旧的
        :param value: 缓存内容
        :return:
        """
        with open(self.path, 'w', encoding='utf-8') as fp:
            json.dump(value, fp, ensure_ascii=False)


    def get_json_cache(self) -> Any:
        """
        获取缓存数据
        :return:
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as fp:
                return json.load(fp)
        except FileNotFoundError:
            ...

    def set_cache(self, value: Any) -> None:
        """
        设置单个缓存数据, 如果内容存在,则替换旧的
        :param value: 缓存内容
        :return:
        """
        with open(self.path, 'w', encoding='utf-8') as fp:
            fp.write(str(value))

    def get_cache(self) -> Any:
        """
        获取缓存数据
        :return:
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as fp:
                return fp.read()
        except FileNotFoundError:
            ...

        # return json.load(fp)



    def set_cache2(self, key: str, value: Any) -> None:
        """
        设置单个字典缓存, 如果内容存在,则替换旧的
        :return:
        """
        with open(self.path, 'w', encoding='utf-8') as fp:
            fp.write(str({key: value}))

    def delete_cache(self) -> None:
        """删除缓存文件"""

        if not os.path.exists(self.path):
            raise FileNotFoundError(f"您要删除的缓存文件不存在 {self.path}")
        os.remove(self.path)

    @classmethod
    def delete_all_cache(cls) -> None:
        """
        清除所有缓存文件
        :return:
        """
        CACHE_DIR = HandlePath().CACHE_DIR

        # 列出目录下所有文件，生成一个list
        list_dir = os.listdir(CACHE_DIR)
        for i in list_dir:
            # 循环删除文件夹下得所有内容
            os.remove(CACHE_DIR + i)


if __name__ == '__main__':
    # HandleCache(filename=None).delete_all_cache()
    # print(ast.literal_eval(HandleCache('cases_cache.json').get_cache())['login_01'])
    print(HandleCache(filename='cases_cache.json').get_cache()['login_01'])
