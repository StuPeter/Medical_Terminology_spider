#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/18
# @Author  : 圈圈烃
# @File    : get_ip
# @description: 建立IP池
#
#


from bs4 import BeautifulSoup
import requests
import re


def get_html(url):
    "get html from the url"
    pattern = re.compile(r'//(.*?)/')
    Host_url = pattern.findall(url)[0]
    headers = {
        "Host": Host_url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    proxies = {"http": "http://103.109.58.242:8080", }   # 设置代理
    res = requests.get(url, headers=headers, timeout=5)
    print("Successfully get html of " + url)
    return res.text


def get_data5u_free_ip():
    url_list = [
        "http://www.data5u.com/free/index.shtml",
        "http://www.data5u.com/free/gngn/index.shtml",
        "http://www.data5u.com/free/gnpt/index.shtml",
        "http://www.data5u.com/free/gwgn/index.shtml",
        "http://www.data5u.com/free/gwpt/index.shtml"
    ]
    for i in range(len(url_list)):
        res_text = get_html(url_list[i])
        # print(res_text)
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find_all("ul", class_="l2")
        for tag in tags:
            ip = tag.span.li.get_text()
            port_1 = tag.find("li", class_="port GEGEA")
            port_2 = tag.find("li", class_="port BGBEGE")
            port_3 = tag.find("li", class_="port GEGEI")
            if ~len(port_1):
                port = port_1.get_text()
            elif ~len(port_2):
                port = port_2.get_text()
            elif ~len(port_3):
                port = port_3.get_text()
            print(ip, "  ", port)


"https://www.kuaidaili.com/ops/proxylist/1/"
"http://www.xsdaili.com/dayProxy/2018/7/1.html"
"https://proxy.mimvp.com/free.php"

def main():
    get_data5u_free_ip()


if __name__ == '__main__':
    main()