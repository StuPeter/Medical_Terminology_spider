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
    """
    获取网页页面
    :param url: url
    :return:
    """
    try:
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
        res.encoding = res.apparent_encoding
        print("Get the " + url + " successfully ")
        return res.text
    except:
        print("Get the " + url + " failed ")


def save_ip(data):
    """
    保存ip信息到txt
    :param data: must be list
    :return:
    """
    try:
        print("We got total of " + str(len(data)) + " data.")
        with open("Ip_Pools/ip_pools.txt", "a") as f:
            for i in range(len(data)):
                f.write(data[i])
            f.close()
            check_ip("Ip_Pools/ip_pools.txt")   # 查重
            print("Ip pools file saved successfully")
    except:
        print("Ip pools file save failed")


def check_ip(path):
    """
    ip 查重
    :param path: file path
    :return:
    """
    try:
        # 读取文件查重
        data_list = []
        with open(path, "r") as fr:
            lines = fr.readlines()
            fr.close()
        for line in lines:
            data_list.append(line)
        new_data_list = list(set(data_list))    # 查重
        # print(data_list)
        print("The text has a total of " + str(len(data_list)) + " data.")
        print("After checking, there are now " + str(len(new_data_list)) + " pieces of data.")
        # 保存文件
        with open(path, "w") as f:
            for i in range(len(new_data_list)):
                f.write(new_data_list[i])
            f.close()
            print("Ip pools file check successfully")
    except:
        print("Ip pools file check failed")


def get_data5u_free_ip():
    """
    爬取无忧代理的免费ip
    :return:
    """
    url_list = [
        "http://www.data5u.com/free/index.shtml",
        "http://www.data5u.com/free/gngn/index.shtml",
        "http://www.data5u.com/free/gnpt/index.shtml",
        "http://www.data5u.com/free/gwgn/index.shtml",
        "http://www.data5u.com/free/gwpt/index.shtml"
    ]
    ip_list_sum = []

    for i in range(5):
        res_text = get_html(url_list[i])
        # 获取li标签中的IP信息
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find_all("ul", class_="l2")
        for tag in tags:
            ip_list = []
            ip_info_format = ""
            sps = tag.find_all("li")
            for sp in sps:
                ip_info = sp.get_text()
                ip_list.append(ip_info)
            for j in range(len(sps)):
                # 格式化IP信息
                if j == len(sps) - 1:
                    ip_info_format += str(ip_list[j]) + "\n"
                else:
                    ip_info_format += str(ip_list[j]) + "___"
            ip_list_sum.append(ip_info_format)
    # print(ip_list_sum)
    save_ip(ip_list_sum)


def get_kuaidaili_free_ip():
    """
    爬取快代理的免费ip
    :return:
    """
    url_list = "https://www.kuaidaili.com/ops/proxylist/1/"
    ip_list_sum = []

    for i in range(10):  # 获取页数
        res_text = get_html("https://www.kuaidaili.com/ops/proxylist/" + str(i+1) + "/")
        # 获取li标签中的IP信息
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find_all("div", id="freelist")
        for tag in tags:
            ip_list = []
            sps = tag.find_all("td")
            # print(tag)
            for sp in sps:
                ip_info = sp.get_text()
                ip_list.append(ip_info)
            # print(ip_list)
            for j in range(10):     # 每页100条数据
                ip_info_format = ""
                for k in range(8):   # 每条6个内容
                    if k == 7:
                        ip_info_format += str(ip_list[(j * 8 + k)]) + "\n"
                    else:
                        ip_info_format += str(ip_list[(j * 8 + k)]) + "___"
                # print(ip_info_format)
                ip_list_sum.append(ip_info_format)
    # print(len(ip_list_sum))
    save_ip(ip_list_sum)


def get_xsdaili_free_ip():
    """
    爬取小舒代理的免费ip
    :return:
    """
    url = "http://www.xsdaili.com/"
    url_list = []
    home_page = get_html(url)
    home_soup = BeautifulSoup(home_page, "html.parser")
    home_tags = home_soup.find_all("div", class_="title")
    for home_tag in home_tags:
        home_url = home_tag.a["href"]
        new_url = "http://www.xsdaili.com" + str(home_url)
        url_list.append(new_url)
    # print(url_list)
    ip_list_sum = []
    for i in range(len(url_list)):  # 页面页数
        res_text = get_html(url_list[i])
        # 获取div标签中的IP信息
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find("div", class_="cont")
        ip_info = tags.get_text()
        ip_info_temp = ip_info.replace("\r\n\t\t\t\t\t\t\t", "")
        ip_list = re.split(r'[:@# \] ]', ip_info_temp)      # 分割字符串
        for j in range(100):    # 每页100条数据
            ip_info_format = ""
            for k in range(6):  # 每条6个内容
                if k == 5:
                    ip_info_format += str(ip_list[(j * 6 + k)]) + "\n"
                else:
                    ip_info_format += str(ip_list[(j * 6 + k)]) + "___"
            # print(ip_info_format)
            ip_list_sum.append(ip_info_format)
    # print(len(ip_list_sum))
    save_ip(ip_list_sum)


def ip_format(read_path, save_path):
    """将搜集的ip进行格式化转换，二次查重"""
    data_list = []
    with open(read_path, "r") as fr:
        lines = fr.readlines()
        fr.close()
    for line in lines:
        new_line = line.split("___")
        ip_format_line = new_line[0].replace(" ", "") + ":" + new_line[1] + "\n"
        # print(ip_format_line)
        data_list.append(ip_format_line)
    with open(save_path, "a") as fs:
        for i in range(len(data_list)):
            fs.write(data_list[i])
        fs.close()
        print("Ip format file saved successfully")
        fs.close()


def ip_test(ip_proxies):
    """ip可用性验证"""
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

    proxies = {"http": "http://" + ip_proxies, }   # 设置代理
    res = requests.get(url, headers=headers, proxies=proxies, timeout=2)
    # 解析网页
    soup = BeautifulSoup(res.text, "html.parser")
    info_list = soup.find_all("p", {"class": "getlist pl10"})
    for info in info_list:
        print(info.get_text())


def main():
    # 获取ip建立IP池
    # get_data5u_free_ip()
    # get_kuaidaili_free_ip()
    # get_xsdaili_free_ip()
    # 筛选ip进行查重
    # ip_format("Ip_Pools/ip_pools.txt", "Ip_Pools/ip_format_pools.txt")
    # check_ip("Ip_Pools/ip_format_pools.txt")
    # 验证ip可用性
    with open("Ip_Pools/ip_format_pools.txt", "r") as fr:
        lines = fr.readlines()
        fr.close()
        count = 0
        for line in lines:
            count += 1
            ip_proxies = line.replace("\n", "")
            try:
                ip_test(ip_proxies)
                with open("Ip_Pools/ip_use.txt", "a") as fs:
                    fs.write(ip_proxies + "\n")
            except:
                pass
                # print("ip不可用")
            print("验证中......%.2f%%" %(count/len(lines)*100))
        print("验证完毕")


if __name__ == '__main__':
    main()