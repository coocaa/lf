#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 10:34
# @Author  : liuxw20

from configparser import ConfigParser
from utils.handler_path.path_contr import HandlePath


class HandleConf(ConfigParser):
    """创建对象时,直接加载配置文件"""

    def __init__(self, conf_file):
        super().__init__()
        self.read(conf_file, encoding='utf-8')

# 生成配置文件对象
conf = HandleConf(HandlePath.CONF_PATH)



