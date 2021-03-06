#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/26
# @Author  : 圈圈烃
# @File    : get_error_html
# @Description:
#
#
import requests
import time
import os
import random


def get_html(url, ip_proxies, user_agent, save_path):
    """
    获取词条的详情页面
    :param url: 词条链接
    :param ip_proxies: 代理ip
    :param user_agent: 浏览器标识
    :param save_path: html文件保存路径
    :return:
    """
    proxies = {"http": "http://" + ip_proxies, }   # 设置代理
    headers = {
        "Host": "baike.baidu.com",
        "User-Agent": user_agent,                      # 设置浏览器头
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://baike.baidu.com/wikitag/taglist?tagId=75953",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    res = requests.post(url, headers=headers, proxies=proxies, timeout=5)
    res.encoding = "utf-8"
    # print(res.text)
    # 抓取错误页面，主动报异常
    if res.text.find("百度百科错误页") != -1:  # 错误页面
        raise AttributeError('错误页面')
    elif res.text.find("ERRO: Cache Access Denied") != -1:  # 错误页面
        raise AttributeError('错误页面')
    elif res.text.find("错误: 您所请求的网址（URL）无法获取") != -1:  # 错误页面
        raise AttributeError('错误页面')
    elif res.text.find("403 Forbidden") != -1:  # 错误页面
        raise AttributeError('错误页面')
    elif res.text.find("锟斤") != -1:  # 错误页面
        raise AttributeError('错误页面')
    with open(save_path, 'w', encoding='utf-8') as fs:
        fs.write(res.text)
        fs.close()


def re_get_html():
    """
    遍历文件夹
    :param work_path: 需要遍历的文件夹根目录
    :return:
    """
    work_path = "Medical_txt_data\\error"  # 错误页面存放路径
    list_path = "Medical_txt_data\\medical_list\\2018_07_30_75953_medical_list_sum.txt"  # 错误页面所属类路径
    available_ip_path = "Ip_Pools\\2018_07_30_ip_use.txt"  # 目前可用代理ip保存路径
    user_agent_path = "User_Agent\\user_agent_pools.txt"
    # 读取列表
    med_url_list = []
    med_name_list = []
    with open(list_path, "r") as fmr:
        med_lines = fmr.readlines()
        for med_line in med_lines:
            med_line_new = med_line.split("---")
            med_name_list.append(med_line_new[0].replace("/", "-").replace("\\", "-"))  # 替换"\","\\",防止被认为是路径
            med_url_list.append(med_line_new[1].replace("\n", ""))
    # 读取UA代理
    user_agent_list = []
    with open(user_agent_path, "r") as fur:
        ua_lines = fur.readlines()
        for ua_line in ua_lines:
            new_ua_line = ua_line.replace("\n", "")
            user_agent_list.append(new_ua_line)
    # 读取可用的IP代理
    ip_use_list = []
    with open(available_ip_path, "r") as fr:
        ip_use_lines = fr.readlines()
        for ip_use_line in ip_use_lines:
            ip_use_line_new = ip_use_line.replace("\n", "")
            ip_use_list.append(ip_use_line_new)
    # 读取错误页面的名称
    index_list = []
    re_url_list = []
    re_name_list = []
    for parent, dirnames, filenames in os.walk(work_path, followlinks=True):
        for filename in filenames:
            index_list.append(med_name_list.index(filename.replace(".html", "")))
            re_url_list.append(med_url_list[med_name_list.index(filename.replace(".html", ""))])
            re_name_list.append(filename.replace(".html", ""))
    # 重新下载，保存页面
    begin = 0  # 断点记录
    for i in range(len(ip_use_list)):
        ip_index = random.randint(0, len(ip_use_list))
        print("目前正在使用第" + str(ip_index) + "个IP代理")
        try:
            for j in range(begin, len(re_url_list)):
                html_save_path = "Name_Url_data/error_1/" + re_name_list[j] + ".html"

                get_html(url=re_url_list[j], ip_proxies=ip_use_list[ip_index],
                         user_agent=user_agent_list[random.randint(0, len(user_agent_list) - 1)], save_path=html_save_path)
                begin = j + 1
                print("第" + str(j) + "个页面保存成功>>>>>>>>>>>>>>>%.2f%%" % (begin / len(re_url_list) * 100))
            break
        except Exception as e:
            print(e)
            print(str(j) + "页面保存失败！！！！！")


def main():
    re_get_html()


if __name__ == '__main__':
    main()

