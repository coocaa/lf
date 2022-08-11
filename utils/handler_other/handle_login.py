#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/9 18:37
# @Author  : liuxw20
import requests

from utils.handler_cache.cache_control import HandleCache
from utils.handler_conf.conf_control import conf
from utils.handler_jsonpath.jsonpath_control import get_value
from utils.handler_log.log_control import log_error
from utils.handler_path.path_contr import HandlePath


class HandleLogin:
    """
    处理登录--token,cookie
    """

    def handle_login(self):
        token, cookie = self.get_token_cookie()
        HandleCache('cookie').set_cache(cookie)
        self.write_token(token)

    def get_token_cookie(self):
        """
        这里处理逻辑
        :return:
        """
        response = self.login()
        # 1.提取cookie
        cookie = ''
        for key, value in response.cookies.items():
            _cookie = key + "=" + value + ";"
            # 拿到登录的cookie内容，cookie拿到的是字典类型，转换成对应的格式
            cookie += _cookie

        # 2.提取token
        try:
            token = get_value(response.json(), 'token')[0]
            return token, cookie

        except Exception as e:
            log_error.logger.error(f'提取登录token失败, 请检查响应内容是否存在"token"关键字')
            return '', cookie

    def write_token(self, token):
        """
        :param token:
        :return:
        """
        new_token = self.handler_token(token)

        options = conf.options("token")
        conf.set('token', options[2], new_token)
        conf.write(fp=open(HandlePath.CONF_PATH, 'w', encoding='utf-8'))

    def handler_token(self, token):
        """

        :param token:
        :return:
        """
        options = conf.options("token")
        value = conf.get('token', options[1])

        if '"' in value:
            value = value.replace('"', '')
            return value + token
        elif "'" in value:
            value = value.replace("'", '')
            return value + token
        else:
            return value + token

    def login(self):
        """
        处理登录
        :return:
        """
        # 1.获取url
        url = conf.get('env', 'login_url')
        # 2.获取请求头
        headers = {}
        headers.update(eval(conf.get('env', 'headers')))

        # 3.获取登录参数
        data = {}
        for item in conf.options("account"):
            data[item] = conf.get('account', item)

        # 4.发送登录请求
        response = requests.post(url=url, json=data, headers=headers, verify=True)

        return response


if __name__ == '__main__':
    print(HandleLogin().login().json())
