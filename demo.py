#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 18:07
# @Author  : liuxw20
from utils.handler_cache.cache_control import HandleCache
from utils.handler_conf.conf_control import conf
from utils.handler_path.path_contr import HandlePath

# url='/api/v1/work/spu/approval/spuApplyDetails/$url_params{id}'
# replace_key='$url_params{id}'
# jsonpath_dates={}
#
# if "$url_param" in replace_key:
#     _url = url.replace(replace_key, str(5))
#     jsonpath_dates['$.url'] = _url
# else:
#     jsonpath_dates[replace_key] = 5
#
# print(url)
# print(jsonpath_dates)


# history_path = HandlePath.REPORT_DIR + 'history.json'
# print(history_path)
# def fun():
#     return 'xx','aa'
# a,b=fun()
# print(type(a))
# print(b)
# x='HandlePath.CONF_PATH'
# options = conf.options("token")
# print(options)
# data=conf.get('token',options[1])
# a=data.replace("'",'')
# a=data.replace('"','')
# print(a+x)
# conf.set('token', options[1], str(token))
# # 将token写入配置文件
# conf.write(fp=open(HandlePath.CONF_PATH, 'w', encoding='utf-8'))

# cache_data = HandleCache('cases_cache.json').get_json_cache()['login_01']
# print(cache_data)
# replace_key='$url_params'
# url='http://api.lemonban.com/futureloan/member/recharge/$url_params{id}'
# x=url.replace(replace_key, str(46))
# print(x)

# data = {'apicode':
#             {'assert_type': 'response', 'jsonpath': '$.code', '==': 0},
#         'username':
#             {'assert_type': 'response', 'jsonpath': '$.data.id', '==': 17741}}
# i = 0
# expect_result = {}
# for name, item in data.items():
#     data = {}
#     i += 1
#
#     for key, value in item.items():
#         if key == 'assert_type':
#             data[value] = key
#         else:
#             if key == 'jsonpath':
#                 data[item.get('assert_type')] = value
#             else:
#                 data[key] = value
#     expect_result[i] = data
# print(expect_result)

def fun():
    try:
        x=2
        return x,True
    except Exception as e:

        return '22',e
    # finally:
    #     return '22'
a,b=fun()
print(a)