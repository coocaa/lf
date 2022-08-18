#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/8 16:12
# @Author  : liuxw20

import requests

from utils.handler_conf.conf_control import conf
from utils.handler_log.log_control import log_error
from utils.handler_other.common import get_report_html
from utils.handler_time.time_control import now_date_time


class WeChatSend:
    """
    企业微信通知封装
    """

    def __init__(self, report_data: dict):
        self.report_data = report_data
        self.curl = conf.get('WeChat', 'webhook')
        self.headers = {"Content-Type": "application/json"}

    def send_main(self):
        """ 发送企业微信通知 """
        text = f"""【{conf.get('other', 'project_name')}自动化通知】
                >测试环境：<font color=\"info\">{conf.get('other', 'env')}</font>
                >测试负责人：@{conf.get('other', 'author')}
                >
                > **执行结果**
                ><font color=\"info\">成  功  率  : {self.report_data['pass_rate']}%</font>
                >用例  总数：<font color=\"info\">{self.report_data['all']}</font>                                    
                >成功用例数：<font color=\"info\">{self.report_data['success']}</font>
                >失败用例数：`{self.report_data['fail']}个`
                >异常用例数：`{self.report_data['error']}个`
                >跳过用例数：<font color=\"warning\">{self.report_data['skip']}个</font>
                >用例执行时长：<font color=\"warning\">{self.report_data['runtime']} s</font>
                >时间：<font color=\"comment\">{now_date_time()}</font>
                >
                >非相关负责人员可忽略此消息。
                >测试报告，点击查看>>[测试报告入口](http://{get_report_html()})"""

        self.send_markdown(text)

    def send_markdown(self, content):
        """
        发送 MarkDown 类型消息
        :param content: 消息内容，markdown形式
        :return:
        """
        _data = {"msgtype": "markdown", "markdown": {"content": content}}
        response = requests.post(url=self.curl, json=_data, headers=self.headers)
        if response.json()['errcode'] != 0:
            log_error.logger.error(response.json())
            raise ValueError("企业微信「MarkDown类型」消息发送失败")

    def send_text(self, content, mobile_list=None):
        """
        发送文本类型通知
        :param content: 文本内容，最长不超过2048个字节，必须是utf8编码
        :param mobile_list: 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
        :return:
        """
        _data = {"msgtype": "text", "text": {"content": content, "mentioned_list": None,
                                             "mentioned_mobile_list": mobile_list}}

        if mobile_list is None or isinstance(mobile_list, list):
            # 判断手机号码列表中得数据类型，如果为int类型，发送得消息会乱码
            if len(mobile_list) >= 1:
                for i in mobile_list:
                    if isinstance(i, str):
                        res = requests.post(url=self.curl, json=_data, headers=self.headers)
                        if res.json()['errcode'] != 0:
                            log_error.logger.error(res.json())
                            raise ValueError("企业微信「文本类型」消息发送失败")

                    else:
                        raise TypeError("手机号码必须是字符串类型.")
        else:
            raise ValueError("手机号码列表必须是list类型.")

    def _upload_file(self, file):
        """
        先将文件上传到临时媒体库
        """
        key = self.curl.split("key=")[1]
        url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"
        data = {"file": open(file, "rb")}
        res = requests.post(url, files=data).json()
        return res['media_id']

    def send_file_msg(self, file):
        """
        发送文件类型的消息
        @return:
        """

        _data = {"msgtype": "file", "file": {"media_id": self._upload_file(file)}}
        res = requests.post(url=self.curl, json=_data, headers=self.headers)
        if res.json()['errcode'] != 0:
            log_error.logger.error(res.json())
            raise ValueError("企业微信「file类型」消息发送失败")


if __name__ == '__main__':
    ...
