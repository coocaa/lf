#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 16:18
# @Author  : liuxw20
import logging
import colorlog
from logging import handlers
from utils.handler_path.path_contr import HandlePath


class HandlerLog:
    """
    日志封装，可设置不同等级的日志颜色
    """

    def __init__(self, filename, when="D"):
        # 1.创建日志处理器对象--默认name是root
        self.logger = logging.getLogger(filename)

        # 2.获取格式化后的颜色
        formatter = self.log_color()

        # 3.设置输出日志的格式
        format_str = logging.Formatter(fmt='%(asctime)s %(filename)s[line:%(lineno)d]-[%(levelname)s]: %(message)s')

        # 4.设置日志收集器的等级
        self.logger.setLevel(logging.DEBUG)

        # 5.往终端上输出
        screen_output = logging.StreamHandler()
        screen_output.setLevel(logging.DEBUG)  # 输出级别
        screen_output.setFormatter(formatter)  # 输出格式

        # 6.往文件里写入
        time_rotating = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=3, encoding='utf-8')
        time_rotating.setFormatter(format_str)  # 设置文件的写入格式

        # 把日志处理器对象加到logger里
        self.logger.addHandler(screen_output)
        self.logger.addHandler(time_rotating)
        # self.log_path = HandlePath.LOG_DIR

    def log_color(self):
        """ 设置日志颜色 """
        log_color_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }

        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s %(filename)s[line:%(lineno)d]-[%(levelname)s]: %(message)s',
            log_colors=log_color_config)

        return formatter


log_info = HandlerLog(HandlePath.log_info_path)
log_error = HandlerLog(HandlePath.log_error_path)
log_warning = HandlerLog(HandlePath.log_warning_path)

if __name__ == '__main__':
    log_info.logger.info('fefefa')
    log_error.logger.error('fefefa')
    log_warning.logger.warning('fefefa')
