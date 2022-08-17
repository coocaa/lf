#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 22:41
# @Author  : liuxw20
from utils.handler_cache.cache_control import cases_cache, HandleCache
from utils.handler_log.log_control import log_error
from utils.handler_other.common import get_case_files
from utils.handler_path.path_contr import HandlePath
from utils.handler_yaml.yaml_analysis import AnalysisYamlData



def set_cases_cache():
    """
    获取所有用例，写入缓存文件
    :return:
    """
    for file_path in get_case_files(data_dir=HandlePath.DATA_DIR):
        case_list = AnalysisYamlData(file_path).analysis(case_id_mark=True)
        for case in case_list:
            for key, value in case.items():  # key==case_id
                # 判断 case_id 是否已存在--抛异常
                if key in cases_cache.keys():
                    msg = f"case_id: {key} 重复了, 请修改case_id\n 文件路径: {file_path}"
                    log_error.logger.error(msg)
                    raise ValueError(msg)
                else:
                    # 将每条用例存入字典
                    HandleCache.set_cases_cache(key, value)


set_cases_cache()