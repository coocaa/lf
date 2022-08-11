#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/30 23:06
# @Author : liuxw20

from enum import Enum


class InformTypeEnum(Enum):
    """
    测试结果自动通知方式
    """

    DING_TALK = 1  # 钉钉通知

    WECHAT = 2  # 微信通知

    EMAIL = 3  # 邮箱通知

    FLY_BOOK = 4  # 飞书通知
