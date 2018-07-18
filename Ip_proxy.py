#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/18
# @Author  : 圈圈烃
# @File    : Ip_proxy
# @description: IP代理可用性查询
#
#


import requests
from bs4 import BeautifulSoup


def ip_test():
    url = "http://ip.chinaz.com/"
    headers = {
        "Host": "ip.chinaz.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://blog.csdn.net/Winterto1990/article/details/51220307",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    proxies = {"http": "http://122.246.51.228:8010", }   # 设置代理
    res = requests.get(url, headers=headers, proxies=proxies)
    # 解析网页
    soup = BeautifulSoup(res.text, "html.parser")
    info_list = soup.find_all("p", {"class": "getlist pl10"})
    for info in info_list:
        print(info.get_text())


def main():
    ip_test()


if __name__ == '__main__':
    main()


