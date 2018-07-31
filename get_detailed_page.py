#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/23
# @Author  : 圈圈烃
# @File    : get_detailed_page
# @Description: 获取详细的词条页面
#
#
import requests
import random
import time
import os


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


def mkdir(path):
    """
    创建文件夹
    :param path: 路径
    :return:
    """
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("文件创建成功")
    else:
        print("文件已经存在")


def main():
    today_date = time.strftime("%Y_%m_%d")  # 当前日期
    # today_date = "2018_07_26"
    user_agent_path = "User_Agent\\user_agent_pools.txt"
    available_ip_path = "Ip_Pools\\2018_07_31_ip_use.txt"  # 目前可用代理ip保存路径
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
    # 信息获取
    begin_list = 1  # 分类断点 (!注意参数设置)
    tagId_list = ["75953", "75954", "75955", "75956"]
    for tagId_num in range(begin_list, 4):  # 四类遍历 (!注意参数设置)
        begin_page = 0  # 页面断点 (!注意参数设置)
        html_save_dir = "Medical_txt_data\\medical_html_" + tagId_list[tagId_num]
        mkdir(html_save_dir)
        list_save_path = "Medical_txt_data\\medical_list\\" + today_date + "_" + tagId_list[tagId_num] + \
                         "_medical_list_sum.txt"  # 列表文件保存路径
        # 读取医学术语和对应链接
        med_url_list = []
        med_name_list = []
        with open(list_save_path, "r") as fmr:
            med_lines = fmr.readlines()
            for med_line in med_lines:
                med_line_new = med_line.split("---")
                med_name_list.append(med_line_new[0].replace("/", "-").replace("\\", "-"))    # 替换"\","\\",防止被认为是路径
                med_url_list.append(med_line_new[1].replace("\n", ""))
        # 保存页面
        while begin_page < len(med_url_list):
            ip_index = random.randint(0, len(ip_use_list))
            print("目前正在使用第" + str(ip_index) + "个IP代理")
            try:
                for j in range(begin_page, len(med_url_list)):
                    html_save_path = html_save_dir + "\\" + med_name_list[j] + ".html"
                    get_html(url=med_url_list[j], ip_proxies=ip_use_list[ip_index],
                             user_agent=user_agent_list[random.randint(0, len(user_agent_list)-1)],
                             save_path=html_save_path)
                    begin_page += 1
                    print(tagId_list[tagId_num] + ":" + str(j) + "个页面保存成功>>>>>>>>>>>>>>>%.2f%%"
                          % (begin_page/len(med_url_list)*100))
                break
            except Exception as e:
                print(e)
                print(tagId_list[tagId_num] + ":" + str(j) + "页面保存失败！！！！！")
        print("----------------------" + tagId_list[tagId_num] + "保存成功" + "----------------------")


if __name__ == '__main__':
    main()

