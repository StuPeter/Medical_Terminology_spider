#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/9/25
# @Author  : 圈圈烃
# @File    : add_detailed_page
# @Description:后期补充词条
#

from urllib.parse import unquote
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import re
import random
import time
import os


def get_html(url, save_path):
    """
    获取词条的详情页面
    :param url: 词条链接
    :param ip_proxies: 代理ip
    :param save_path: html文件保存路径
    :return:
    """
    headers = {
        "Host": "baike.baidu.com",
        "User-Agent": "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",                      # 设置浏览器头
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://baike.baidu.com/wikitag/taglist?tagId=75953",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    res = requests.post(url, headers=headers, timeout=5)
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


def parser_html(html_path, filename, collection):
    """
    解析百度百科词条页面
    :param html_path: 百科HTML页面路径
    :param filename: 文件名
    :param collection: 数据库文档
    :return: 字典
    """
    with open(html_path, "r", encoding="utf-8") as fmr:
        med_res = fmr.read()
    soup = BeautifulSoup(med_res, 'html.parser')
    # 创建字典
    try:
        content = soup.find_all(attrs={"name": "description"})[0]['content']
        doc = {
            "名称": filename,
            "简介": content.replace("...", "")
        }
    except Exception as e:
        doc = {
            "名称": filename,
            "简介": None,
        }
    # 解析页面
    key_tags = soup.find_all('div', class_="para-title level-2")
    value_lists = []
    key_lists = []
    for key_tag in key_tags:
        # 字典键
        key_lists.append(key_tag.h2.contents[-1])
        # 解析第一段<div class=para ...>
        value_tags = key_tag.next_sibling.next_sibling
        value_list = []
        for value_new_tags in value_tags.contents:
            pattern = re.compile(r'<.*?>')
            value_new_tag = pattern.sub("", str(value_new_tags))
            value_list.append(value_new_tag)
        # 解析同一大段中的小段<div class=para ...>
        count = 1
        for i in range(1000):   # 百度百科页面“<div class=para ...>”的并列数量
            vl = eval("value_tags" + count*".next_sibling")
            try:
                if vl == '\n':
                    count += 1
                    value_list.append(vl.string)
                elif vl['class'][0] == 'para':
                    count += 1
                    for vl_con in vl.contents:
                        pattern = re.compile(r'<.*?>')
                        vl_new_con = pattern.sub("", str(vl_con))
                        # print(vl_new_con)
                        value_list.append(vl_new_con.replace("\n", ""))
                    # print(type(vl.contents))
                else:
                    break
            except Exception as e:
                break
        # 同一段内容合并
        value_new_list = ""
        for j in range(len(value_list)):
            value_new_list += value_list[j]
        value_lists.append(value_new_list)
    # 组成字典
    for i in range(len(key_lists)):
        doc[key_lists[i]] = value_lists[i]
    print(doc)
    # 存入数据库
    # collection.insert_one(doc)


def main():
    # 连接MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    # 获取名字为 medical_db 的数据库对象
    db = client.medical_new_detial_db
    # 获取名字为 disease
    collection_1 = db.disease
    collection_2 = db.drug
    collection_3 = db.diagnosis
    collection_4 = db.chinese_medicine

    save_path = "Medical_txt_data/add_disease_html/"
    # url = input("请输入需要补充的链接地址（百度百科词条页面）：")
    url = "https://baike.baidu.com/item/" + "膈疝"
    name = unquote(url, encoding='utf-8').split('/')[-1]
    html_save_path = save_path + name + ".html"
    get_html(url, save_path=html_save_path)
    print("保存成功...")
    parser_html(html_save_path, name, collection_1)
    print("数据库写入成功")


if __name__ == '__main__':
    main()

