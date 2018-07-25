#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/23
# @Author  : 圈圈烃
# @File    : get_detailed_page
# @description: 获取详细的词条页面
#
#


import requests
import time
import random


def get_html(url, ip_pro, ua, save_path):
    """获取百度百科医疗术语详情页面"""
    proxies = {"http": "http://" + ip_pro, }   # 设置代理
    headers = {
        "Host": "baike.baidu.com",
        "User-Agent": ua,                      # 设置浏览器头
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
    if (res.text.find("百度百科错误页") != -1):  # 错误页面
        raise AttributeError('错误页面')
    with open(save_path, 'w', encoding='utf-8') as fs:
        fs.write(res.text)
        fs.close()


def main():
    # today_date = time.strftime("%Y_%m_%d")  # 当前日期
    today_date = "2018_07_26"
    list_save_path = "Name_Url_data/medical_list_" + today_date + "/" + today_date + "_medical_list_sum.txt"
    user_agent_path = "User_Agent_Pools/user_agent_pools.txt"
    available_ip_path = "Ip_Pools/ip_use_6.txt"  # 目前可用ip地址
    # 读取医学术语和对应链接
    med_url_list = []
    med_name_list = []
    with open(list_save_path, "r") as fmr:
        med_lines = fmr.readlines()
        for med_line in med_lines:
            med_line_new = med_line.split("---")
            med_name_list.append(med_line_new[0].replace("/", "-").replace("\\", "-"))    # 替换"\","\\",防止被认为是路径
            med_url_list.append(med_line_new[1].replace("\n", ""))
            # print(med_line_new[0])
            # print(med_line_new[1])
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
    # 保存页面
    begin = 3381  # 断点记录
    for i in range(len(ip_use_list)):
        ip_index = random.randint(0, len(ip_use_list))
        print("目前正在使用第" + str(ip_index) + "个IP代理")
        try:
            for j in range(begin, len(med_url_list)):
                html_save_path = "Name_Url_data/medical_html_" + today_date + "/" + med_name_list[j] + ".html"

                get_html(url=med_url_list[j], ip_pro=ip_use_list[ip_index], \
                         ua=user_agent_list[random.randint(0, len(user_agent_list)-1)], save_path=html_save_path)

                begin = j + 1

                print("第" + str(j) + "个页面保存成功>>>>>>>>>>>>>>>%.2f%%" % (begin/len(med_url_list)*100))
            break
        except:
            print(str(j) + "页面保存失败！！！！！")


if __name__ == '__main__':
    main()

