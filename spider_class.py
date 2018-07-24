#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/17
# @Author  : 圈圈烃
# @File    : spider_class
# @description:
#
#


import requests

#
# class Spider_Medical_Baidu():
#     """医药术语爬虫类"""
#     headers = {
#         "Host": "baike.baidu.com",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#         "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Referer": "https://baike.baidu.com/science/medical",
#         # "Cookie": "BAIDUID=3DD7B34F9D6150DF0D51021532ED0A8A:FG=1; BIDUPSID=3DD7B34F9D6150DF0D51021532ED0A8A; PSTM=1531732931; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1531798081; pgv_pvi=5285199872; H_PS_PSSID=26524_1469_21088_18559_20928; PSINO=5; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1531814395; pgv_si=s3781830656"
#         "Connection": "keep-alive",
#         "Upgrade-Insecure-Requests": 1,
#         "Cache-Control": "max-age=0"
#     }
