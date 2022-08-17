#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/8 16:12
# @Author  : liuxw20
import base64
import hashlib
import hmac
import time
import urllib.parse
from typing import Any
from dingtalkchatbot.chatbot import DingtalkChatbot, FeedLink
from utils.handler_conf.conf_control import conf
from utils.handler_other.common import get_report_html


class DingTalkSend:
    """
    钉钉通知封装
    """

    def __init__(self, report_data: dict):
        self.report_data = report_data
        self.timeStamp = str(round(time.time() * 1000))
        self.sign = self.get_sign()
        # 获取钉钉配置信息
        self.webhook = conf.get('DingTalk', 'webhook') + "&timestamp=" + self.timeStamp + "&sign=" + self.sign
        # 获取 webhook地址
        self.xiao_ding = DingtalkChatbot(self.webhook)

    def get_sign(self) -> str:
        """
        根据时间戳 + "sign" 生成密钥
        :return:
        """
        secret = conf.get('DingTalk', 'secret')
        string_to_sign = f'{self.timeStamp}\n{secret}'.encode('utf-8')
        hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_main(self):
        """
        发送钉钉报告通知
        """
        # 判断如果有失败的用例,@所有人
        is_at_all = False
        if self.report_data['fail'] + self.report_data['error'] > 0:
            is_at_all = True

        text = f"#### {conf.get('other', 'projectName')}自动化通知  " \
               f"\n\n>Python脚本任务: {conf.get('other', 'projectName')}" \
               f"\n\n>环境: {conf.get('other', 'env')}\n\n>" \
               f"执行人: {conf.get('other', 'author')}" \
               f"\n\n>执行结果: {self.report_data['pass_rate']}% " \
               f"\n\n>总用例数: {self.report_data['all']} " \
               f"\n\n>成功用例数: {self.report_data['success']}" \
               f" \n\n>失败用例数: {self.report_data['fail']} " \
               f" \n\n>异常用例数: {self.report_data['error']} " \
               f"\n\n>跳过用例数: {self.report_data['skip']}" \
               f" > ###### 测试报告 [详情](http://{get_report_html()}) \n"

        self.send_markdown(title="【接口自动化通知】", msg=text, is_at_all=is_at_all)

    def send_markdown(self, title: str, msg: str, is_at_all=False, mobiles=None, ) -> None:
        """

        :param is_at_all:
        :param mobiles:
        :param title:
        :param msg:
        markdown 格式
        """
        if mobiles is None:
            self.xiao_ding.send_markdown(title=title, text=msg, is_at_all=is_at_all)
        else:
            if isinstance(mobiles, list):
                self.xiao_ding.send_markdown(title=title, text=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    def send_text(self, msg: str, mobiles=None) -> None:
        """
        发送文本信息
        :param msg: 文本内容
        :param mobiles: 用户电话
        :return:
        """
        if not mobiles:
            self.xiao_ding.send_text(msg=msg, is_at_all=True)
        else:
            if isinstance(mobiles, list):
                self.xiao_ding.send_text(msg=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    def send_link(self, title: str, text: str, message_url: str, pic_url: str) -> None:
        """
        发送link通知
        :return:
        """
        self.xiao_ding.send_link(title=title, text=text, message_url=message_url, pic_url=pic_url)

    def send_feed_link(self, *arg) -> None:
        """发送 feed_lik """

        self.xiao_ding.send_feed_card(list(arg))

    @staticmethod
    def feed_link(title: str, message_url: str, pic_url: str) -> Any:
        """ FeedLink 二次封装 """
        return FeedLink(title=title, message_url=message_url, pic_url=pic_url)


if __name__ == '__main__':
    ...
