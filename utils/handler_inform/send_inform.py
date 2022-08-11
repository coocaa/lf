#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/8 16:12
# @Author  : liuxw20
import json

from utils.handler_inform.ding_talk import DingTalkSend
from utils.handler_inform.fly_book import FlyBookSend
from utils.handler_inform.mail import EmailSend
from utils.handler_inform.wechat import WeChatSend
from utils.handler_path.path_contr import HandlePath
from utils.handler_conf.conf_control import conf
from utils.handler_enum.inform_type_enum import InformTypeEnum




def get_report_data() -> dict:
    """
    测试报告结果清洗,提取业务需要的数据
    """
    # 1.提取测试报告历史数据的文件路径
    history_path = HandlePath.REPORT_DIR + 'history.json'
    with open(history_path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    # 2.提取报告数据
    result = {
        'all': data[-1]['all'],
        'success': data[-1]['success'],
        'fail': data[-1]['fail'],
        'error': data[-1]['error'],
        'pass_rate': data[-1]['pass_rate'],
        'runtime': data[-1]['runtime'],
        'begin_time': data[-1]['begin_time']
    }

    return result


def send_inform():
    # 1.获取测试报告数据
    report_data = get_report_data()
    # 2.获取通知方式对应的方法地址
    inform_mapping = {
        InformTypeEnum.DING_TALK.value: DingTalkSend(report_data).send_main,
        InformTypeEnum.WECHAT.value: WeChatSend(report_data).send_main,
        InformTypeEnum.EMAIL.value: EmailSend(report_data).send_main,
        InformTypeEnum.FLY_BOOK.value: FlyBookSend(report_data).send_main}

    # 3.获取通知方式
    _type = conf.getint('other', 'inform_type')
    if _type != 0:
        # 4.调用发送
        inform_mapping.get(_type)()
