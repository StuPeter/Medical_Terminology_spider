#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/26
# @Author  : 圈圈烃
# @File    : store_data_detial
# @description:
#
#
#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 2018/7/25
# @Author  : 圈圈烃
# @File    : store_data
# @description: 将数据存入MongoDB数据库中
#
#


from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import os


def path_search(work_path):
    """
    便利文件夹
    :param work_path: 需要遍历的文件夹根目录
    :return:
    """
    for parent, dirnames, filenames in os.walk(work_path, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            print('文件名：%s' % filename)
            print('文件完整路径：%s\n' % file_path)


def parser_html(html_path, filename):
    """
    解析百度百科词条页面
    :param html_path: 百科HTML页面路径
    :param filename: 文件名
    :param collection: 数据库文档
    :return: 字典
    """
    with open(html_path, "r", encoding="utf-8") as fmr:
        med_res = fmr.read().replace("<br/>", "").replace("<b>", "").replace("</b>", "")

    soup = BeautifulSoup(med_res, 'html.parser')
    # 创建字典
    content = soup.find_all(attrs={"name": "description"})[0]['content']
    doc = {
        "名称": filename,
        "简介": content.replace("...", "")
    }


    # # 字典键
    # key_list = []
    # k_tags = soup.find_all('li', class_="level1")
    # for k_tag in k_tags:
    #     key_list.append(k_tag.a.string)
    # # print(key_list)
    # # 字典值
    # value_list = []
    # v_tags = soup.find_all('div', class_="para")
    # for v_tag in v_tags:
    #     value_list.append(v_tag.string)
    # # 检测重复
    # vs_tags = soup.find_all('div', class_="lemma-summary")
    # try:
    #     for vs_tag in vs_tags:
    #         need_rm = vs_tag.find('div', class_="para").string
    #         # print(need_rm)
    #     value_list.remove(need_rm)
    # except:
    #     pass
    # # 组成字典
    # for i in range(len(key_list)):
    #     doc[key_list[i]] = value_list[i]
    # print(doc)
    # # collection.insert_one(doc)
    # print("保存成功")


def store_list_detial(read_path):
    """
    将txt文件中的数据写入数据库
    :param read_path: 文件路径
    :param collection: 数据库文档
    :return:
    """
    for parent, dirnames, filenames in os.walk(read_path, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            print(filename)
            parser_html(file_path, filename.replace(".html", ""))


def main():
    """
    # read_path = "Name_Url_data\\drug_html"
    # read_path_1 = "Name_Url_data/diagnosis_list/2018_07_25_medical_list_sum.txt"
    # read_path_2 = "Name_Url_data/chinese_medicine_list/2018_07_26_medical_list_sum.txt"
    # read_path_3 = "Name_Url_data/disease/2018_07_26_medical_list_sum.txt"
    # # 连接MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    # # 获取名字为 medical_db 的数据库对象
    db = client.medical_detial_db
    # # 获取名字为 disease
    collection = db.drug
    # collection_1 = db.diagnosis
    # collection_2 = db.chinese_medicine
    # collection_3 = db.disease
    # # 存入数据
    store_list_detial(read_path, collection)
    # store_list(read_path_1, collection_1)
    # store_list(read_path_2, collection_2)
    # store_list(read_path_3, collection_3)
    # # 关闭客户端
    client.close()
    """
    read_path = "Name_Url_data\\test"
    store_list_detial(read_path)


if __name__ == '__main__':
    main()
