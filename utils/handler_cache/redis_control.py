#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/28 15:28
# @Author : liuxw20

from typing import Any
import redis

from utils.handler_conf.conf_control import conf
from utils.handler_log.log_control import log_error


class HandlerRedis:
    """
    redis 缓存操作封装
    """

    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=conf.get('redis', 'host'),
                port=conf.getint('redis', 'port'),
                password=conf.getint('redis', 'password'),
                db=conf.getint('redis', 'db'),
                decode_responses=True,
                charset='UTF-8', )
        except:
            log_error.logger.error('redis数据连接失败, 请检查配置')
            raise ValueError('redis数据连接失败, 请检查配置')

    def set_string(self, name: str, value: Any, exp_time=None, exp_milliseconds=None, name_not_exist=False,
                   name_exit=False) -> None:
        """
        缓存中写入 str（单个）
        :param name: 缓存名称
        :param value: 缓存值
        :param exp_time: 过期时间（秒）
        :param exp_milliseconds: 过期时间（毫秒）
        :param name_not_exist: 如果设置为True，则只有name不存在时，当前set操作才执行（新增）
        :param name_exit: 如果设置为True，则只有name存在时，当前set操作才执行(修改）
        :return:
        """
        self.redis.set(name, value, ex=exp_time, px=exp_milliseconds, nx=name_not_exist, xx=name_exit)

    def key_exist(self, key: str):
        """
        判断redis中的key是否存在
        :param key:
        :return:
        """

        return self.redis.exists(key)

    def incr(self, key: str):
        """
        使用 incr 方法，处理并发问题
        当 key 不存在时，则会先初始为 0, 每次调用，则会 +1
        :return:
        """
        self.redis.incr(key)

    def get_key(self, name: Any) -> str:
        """
        读取缓存
        :param name:
        :return:
        """
        return self.redis.get(name)

    def set_many(self, *args, **kwargs):
        """
        批量设置
        支持如下方式批量设置缓存
        eg: set_many({'k1': 'v1', 'k2': 'v2'})
            set_many(k1="v1", k2="v2")
        :return:
        """
        self.redis.mset(*args, **kwargs)

    def get_many(self, *args):
        """
        获取多个值
        """
        return self.redis.mget(*args)

    def del_cache(self, name):
        """
        删除单个缓存
        :param name:
        :return:
        """
        self.redis.delete(name)

    def del_all_cache(self):
        """
        删除所有数据
        """
        for key in self.redis.keys():
            self.del_cache(key)
