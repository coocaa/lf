#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/8 19:12
# @Author  : liuxw20
import smtplib
from email.mime.text import MIMEText
from utils.handler_conf.conf_control import conf


class EmailSend:
    """
    发送邮件通知
    """

    def __init__(self, report_data: dict):
        self.report_data = report_data
        self.send_user = conf.get('Email', 'send_user')  # 发件人
        self.email_host = conf.get('Email', 'email_host')  # QQ 邮件 STAMP 服务器地址
        self.stamp_key = conf.get('Email', 'stamp_key')  # STAMP 授权码
        self.send_list = conf.get('Email', 'send_list')  # 收件人
        self.project_name = conf.get('other', 'projectName')

    def send_main(self) -> None:
        """
        发送邮件
        :return:
        """
        user_list = self.send_list.split(',')  # 多个邮箱发送,yaml文件中直接添加  '806029174@qq.com'

        title = self.project_name + "接口自动化报告"
        content = f"""
           各位同事, 大家好:
               自动化用例执行完成，执行结果如下:
               用例运行总数: {self.report_data['all']} 个
               通过用例个数: {self.report_data['success']} 个
               失败用例个数: {self.report_data['fail']} 个
               异常用例个数: {self.report_data['error']} 个
               跳过用例个数: {self.report_data['skip']} 个
               成  功   率: {self.report_data['pass_rate']} %

           **********************************
           jenkins地址：https://121.xx.xx.47:8989/login
           详细情况可登录jenkins平台查看，非相关负责人员可忽略此消息。谢谢。
           """
        self.send_mail(user_list, title, content)


    def send_mail(self, user_list: list, title, content: str) -> None:
        """
        @param user_list: 发件人邮箱
        @param title:
        @param content: 发送内容
        @return:
        """
        user = conf.get('other', 'author') + "<" + self.send_user + ">"
        message = MIMEText(content, _subtype='plain', _charset='utf-8')
        message['Subject'] = title
        message['From'] = user
        message['To'] = ";".join(user_list)
        server = smtplib.SMTP()
        server.connect(self.email_host)
        server.login(self.send_user, self.stamp_key)
        server.sendmail(user, user_list, message.as_string())
        server.close()

    def error_mail(self, error_message: str) -> None:
        """
        执行异常邮件通知
        @param error_message: 报错信息
        @return:
        """
        email = self.send_list
        user_list = email.split(',')  # 多个邮箱发送，config文件中直接添加  '806029174@qq.com'

        title = self.project_name + "接口自动化执行异常通知"
        content = f"自动化测试执行完毕，程序中发现异常，请悉知。报错信息如下：\n{error_message}"
        self.send_mail(user_list, title, content)



if __name__ == '__main__':
    ...
