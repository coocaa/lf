#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 10:34
# @Author  : liuxw20
import random
from faker import Faker

fake = Faker(locale='zh_CN')


def random_fake(value: str) -> str:
    """
    随机数据
    :param value: 指定类别
    :return:
    """

    if value == 'name':  # 姓名
        return fake.name()
    elif value == 'phone':  # 电话
        return fake.phone_number()
    elif value == 'card':  # 身份证
        return fake.ssn()
    elif value == 'email':  # 邮箱
        return fake.email()
    elif value == 'date':  # 日期
        return fake.date()
    elif value == 'address':  # 地址
        return fake.address()
    elif value == 'company':  # 公司
        return fake.company()
    elif value == 'city':  # 城市
        return fake.city()
    elif value == 'text':  # 一段文本
        return fake.text()
    elif value == 'letter':  # 单个字母
        return fake.random_letter()
    elif value == 'str':  # 字符串
        return fake.pystr()


def random_int(mix_value: int = None, max_value: int = None) -> str:
    """
    # 随机整数
    :param mix_value: 最小值
    :param max_value: 最大值
    :return:
    """
    if mix_value and max_value:
        return str(random.randint(mix_value, max_value))
    else:
        return str(random.randint(100, 9999))

def cache(variable):
    """
    处理缓存变量
    :param variable:
    :return:
    """
    result=f'cache({variable})'
    return result