#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 2.0
# @Time    : 2018/7/17
# @Author  : 圈圈烃
# @File    : get_medical_from_baidu
# @Description: 获取词条列表和链接
#
#
import requests
import random
import time
import json
import os


def get_html(page_num, ip_proxies, save_path, tagId):
    """
    获取百度分类页面的词条名称和词条详细页面的链接
    :param page_num: 分页, 其中：疾病症状-74页， 药物-83页， 诊疗方法-26页， 中医-43页
    :param ip_proxies: 代理ip
    :param save_path: json数据的保存路径
    :param tagId: 分类页面，其中：疾病症状-75953， 药物-75954， 诊疗方法-75955， 中医-75956
    :return: json数据文件
    """
    url = "https://baike.baidu.com/wikitag/api/getlemmas"   # 目标链接
    proxies = {"http": "http://" + ip_proxies, }   # 设置代理
    headers = {
        "Host": "baike.baidu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://baike.baidu.com/wikitag/taglist?tagId=" + tagId,
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
        "tagId": tagId,
        "timeout": "3000",
    }
    res = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=5)
    res_json = json.dumps(res.json(), ensure_ascii=False)
    res_json_new_coding = res_json.encode("GBK", "ignore")
    if res_json_new_coding:
        with open(save_path, 'wb+') as f:
            f.write(res_json_new_coding)
            f.close()
    else:
        raise AttributeError("ERROR:json数据为空")


def analysis_json(read_path, save_path):
    """
    解析json数据
    :param read_path: 待读取的json文件
    :param save_path: 待保存的文本文件
    :return:
    """
    # 解析名称和对应的url
    with open(read_path, "r") as fr:
        med_txt = fr.read()
        med_json = json.loads(med_txt)
    for list_num in range(len(med_json['lemmaList'])):
        med_title = med_json['lemmaList'][list_num]['lemmaTitle']
        med_url = med_json['lemmaList'][list_num]['lemmaUrl']
        # 保存数据
        with open(save_path, "a") as fs:
            fs.write(med_title + "---" + med_url + "\n")


def check_medical_list(path):
    """
    医药列表查重
    :param path: 文件路径
    :return:
    """
    file_name = path.split("/")
    try:
        # 读取文件
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
    except Exception as e:
        print(e)
        print(file_name[-1] + "查重失败")


def mkdir(path):
    """
    创建文件夹
    :param path: 路径
    :return:
    """
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print(path + "文件创建成功")
    else:
        print(path + "文件已经存在")


def main():
    # 文件保存路径设置
    today_date = time.strftime("%Y_%m_%d")  # 当前日期
    # today_date = "2018_07_26"  # 当前日期
    available_ip_path = "Ip_Pools\\2018_07_31_ip_use.txt"  # 目前可用代理ip保存路径
    json_save_dir = "Medical_txt_data\\medical_json_" + today_date   # json文件文件夹
    mkdir(json_save_dir)
    # 代理ip读取
    ip_use_list = []
    with open(available_ip_path, "r") as fr:
        ip_use_lines = fr.readlines()
        for ip_use_line in ip_use_lines:
            ip_use_line_new = ip_use_line.replace("\n", "")
            ip_use_list.append(ip_use_line_new)
    # 信息获取
    begin_list = 0   # 分类断点 (!注意参数设置)
    begin_page = 0    # 页面断点 (!注意参数设置)
    tagId_list = ["75953", "75954", "75955", "75956"]
    tagId_pages = ["74", "83", "26", "43"]    # 疾病症状-74页， 药物-83页， 诊疗方法-26页， 中医-43页
    for tagId_num in range(begin_list, 4):   # 四类遍历 (!注意参数设置)
        list_save_dir = "Medical_txt_data\\medical_list\\" + today_date + "_" + tagId_list[tagId_num]
        mkdir(list_save_dir)
        list_save_path = list_save_dir + "_medical_list_sum.txt"  # 列表文件保存路径
        while begin_page < int(tagId_pages[tagId_num]):
            ip_index = random.randint(0, len(ip_use_list) - 1)  # 产生随机代理ip
            try:
                for j in range(begin_page, int(tagId_pages[tagId_num])):  # 修改页数
                    json_save_path = json_save_dir + "\\" + today_date + "_" + tagId_list[tagId_num] + \
                                     "_medical_json_(" + str(j) + ").txt"
                    get_html(page_num=j, ip_proxies=ip_use_list[ip_index], save_path=json_save_path,
                             tagId=tagId_list[tagId_num])
                    analysis_json(json_save_path, list_save_path)
                    print("目前正在使用第" + str(ip_index) + "个IP代理")
                    print(tagId_list[tagId_num] + ":" + str(j) +"页面保存成功")
                break
            except Exception as e:
                print(e)
                print("目前正在使用第" + str(ip_index) + "个IP代理")
                print(tagId_list[tagId_num] + ":" + str(j) +"页面保存失败！！！！！")
        # 词条查重
        check_medical_list(list_save_path)
        print("----------------------" + tagId_list[tagId_num] + "保存成功" + "----------------------")


if __name__ == '__main__':
    main()

