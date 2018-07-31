#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/26
# @Author  : 圈圈烃
# @File    : store_data_detial
# @Description: 将获取的详细数据存入MongoDB数据库中
#
#
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import os


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
    # 存入数据库
    collection.insert_one(doc)


def store_list_detial(read_path, collection):
    """
    将txt文件中的数据写入数据库
    :param read_path: 文件路径
    :param collection: 数据库文档
    :return:
    """
    count = 1
    for parent, dirnames, filenames in os.walk(read_path, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            # print(filename)
            try:
                parser_html(file_path, filename.replace(".html", ""), collection)
                print("第" + str(count) + "个页面成功存入数据库>>>>>>>>>>>>>>>%.2f%%" % (count / len(filenames) * 100))
                count += 1
            except Exception as e:
                print(e)
                print("第" + str(count) + "个页面无法存入数据库！！！>>>>>>>>>>>>>>>%.2f%%" % (count / len(filenames) * 100))
                count += 1


def main():
    read_path_1 = "Medical_txt_data\\medical_html_75953"
    read_path_2 = "Medical_txt_data\\medical_html_75954"
    read_path_3 = "Medical_txt_data\\medical_html_75955"
    read_path_4 = "Medical_txt_data\\medical_html_75956"
    # 连接MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    # 获取名字为 medical_db 的数据库对象
    db = client.medical_new_detial_db
    # 获取名字为 disease
    collection_1 = db.disease
    collection_2 = db.drug
    collection_3 = db.diagnosis
    collection_4 = db.chinese_medicine
    # # 存入数据
    store_list_detial(read_path_1, collection_1)
    print("----------------------db.disease保存成功----------------------")
    store_list_detial(read_path_2, collection_2)
    print("----------------------db.drug保存成功----------------------")
    store_list_detial(read_path_3, collection_3)
    print("----------------------db.diagnosis保存成功----------------------")
    store_list_detial(read_path_4, collection_4)
    print("----------------------db.chinese_medicine保存成功----------------------")

    # # 关闭客户端
    client.close()


if __name__ == '__main__':
    main()

