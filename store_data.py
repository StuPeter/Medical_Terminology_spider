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


def store_list(read_path, collection):
    """
    将txt文件中的数据写入数据库
    :param read_path: 文件路径
    :param collection: 数据库文档
    :return:
    """
    with open(read_path, "r") as fmr:
        med_lines = fmr.readlines()
        for med_line in med_lines:
            med_line_new = med_line.split("---")
            doc = {
                'name': med_line_new[0].replace("/", "-").replace("\\", "-"),
                'url': med_line_new[1].replace("\n", "")
            }
            collection.insert_one(doc)
        # print("保存成功")


def main():
    read_path_1 = "Medical_txt_data\\medical_list\\2018_07_30_75953_medical_list_sum.txt"
    read_path_2 = "Medical_txt_data\\medical_list\\2018_07_30_75954_medical_list_sum.txt"
    read_path_3 = "Medical_txt_data\\medical_list\\2018_07_30_75955_medical_list_sum.txt"
    read_path_4 = "Medical_txt_data\\medical_list\\2018_07_30_75956_medical_list_sum.txt"
    # 连接MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    # 获取名字为 medical_db 的数据库对象
    db = client.medical_new_db
    # 获取名字为 disease
    collection_1 = db.disease
    collection_2 = db.drug
    collection_3 = db.diagnosis
    collection_4 = db.chinese_medicine
    # 存入数据
    store_list(read_path_1, collection_1)
    print("----------------------db.disease保存成功----------------------")
    store_list(read_path_2, collection_2)
    print("----------------------db.drug保存成功----------------------")
    store_list(read_path_3, collection_3)
    print("----------------------db.diagnosis保存成功----------------------")
    store_list(read_path_4, collection_4)
    print("----------------------db.chinese_medicine保存成功----------------------")
    # 关闭客户端
    client.close()


if __name__ == '__main__':
    main()
