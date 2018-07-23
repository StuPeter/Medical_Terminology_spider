#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 2.0
# @Time    : 2018/7/17
# @Author  : 圈圈烃
# @File    : get_medical_from_baidu
# @description:
#
#

import requests
import time
import json
import random


def get_html(page_num, ip_pro, save_path):
    """获取百度百科医疗术语"""
    strtime = time.strftime("%Y_%m_%d")  # 当前日期
    url = "https://baike.baidu.com/wikitag/api/getlemmas"   # 目标链接
    proxies = {"http": "http://" + ip_pro, }   # 设置代理
    headers = {
        "Host": "baike.baidu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://baike.baidu.com/wikitag/taglist?tagId=75953",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "X - Requested - With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    data = {
        "contentLength": "40",
        "filterTags": "[]",
        "fromLemma": "false",
        "limit": "100",
        "page": str(page_num),
        "tagId": "75953",
        "timeout": "3000",
    }
    res = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=5)
    res_json = json.dumps(res.json(), ensure_ascii=False)
    res_json_new_coding = res_json.encode("GBK", "ignore")
    with open(save_path, 'wb+') as f:
        f.write(res_json_new_coding)
        f.close()
    # print("Success get json")


def analysis_json(read_path, save_path):
    """解析获取的json数据"""
    # 解析数据
    strtime = time.strftime("%Y_%m_%d")  # 当前日期
    with open(read_path, "r") as fr:
        med_txt = fr.read()
        med_json = json.loads(med_txt)
    for list_num in range(len(med_json['lemmaList'])):
        med_title = med_json['lemmaList'][list_num]['lemmaTitle']
        med_url = med_json['lemmaList'][list_num]['lemmaUrl']
        # 保存数据
        with open(save_path, "a") as fs:
            fs.write(med_title + "---" + med_url + "\n")
    # print("Success save list")


def check_medical_list(path):
    """
    medical_list 查重
    :param path: file path
    :return:
    """
    file_name = path.split("/")
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
        print(file_name[-1] + "文件共有 " + str(len(data_list)) + " 条数据")
        print("经过查重,现共有 " + str(len(new_data_list)) + " 条数据")
        # 保存文件
        with open(path, "w") as f:
            for i in range(len(new_data_list)):
                f.write(new_data_list[i])
            f.close()
            print(file_name[-1] + "查重成功")
    except:
        print(file_name[-1] + "查重失败")


def main():
    today_date = time.strftime("%Y_%m_%d")  # 当前日期
    list_save_path =  "Name_Url_data/medical_list_" + today_date + "/" + today_date + "_medical_list_sum.txt"
    available_ip_path = "Ip_Pools/ip_use_5.txt"  # 目前可用ip地址
    ip_use_list = []
    with open(available_ip_path, "r") as fr:
        ip_use_lines = fr.readlines()
        for ip_use_line in ip_use_lines:
            ip_use_line_new = ip_use_line.replace("\n", "")
            ip_use_list.append(ip_use_line_new)
    begin = 0   # 断点记录
    for i in range(len(ip_use_list)):
        ip_index = random.randint(0, len(ip_use_list))
        try:
            for j in range(begin, 73):
                json_save_path = "Name_Url_data/medical_json_" + today_date + "/" + today_date + "_medical_json(" + str(
                    j) + ").txt"
                get_html(page_num=j, ip_pro=ip_use_list[ip_index], save_path=json_save_path)
                analysis_json(json_save_path, list_save_path)
                begin = j + 1
                print("目前正在使用第" + str(ip_index) + "个IP代理")
                print(str(j) +"页面保存成功")
            break
        except:
            print("目前正在使用第" + str(ip_index) + "个IP代理")
            print(str(j) +"页面保存失败！！！！！")
    # 词条查重
    check_medical_list(list_save_path)


if __name__ == '__main__':
    main()

