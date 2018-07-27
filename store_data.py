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
        print("保存成功")


def main():
    read_path_1 = "Name_Url_data/drug_list/2018_07_24_medical_list_sum.txt"
    read_path_2 = "Name_Url_data/diagnosis_list/2018_07_25_medical_list_sum.txt"
    read_path_3 = "Name_Url_data/chinese_medicine_list/2018_07_26_medical_list_sum.txt"
    read_path_4 = "Name_Url_data/disease_list/2018_07_23_medical_list_sum.txt"
    # 连接MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    # 获取名字为 medical_db 的数据库对象
    db = client.medical_db
    # 获取名字为 disease
    collection_1 = db.drug
    collection_2 = db.diagnosis
    collection_3 = db.chinese_medicine
    collection_4 = db.disease
    # 存入数据
    store_list(read_path_1, collection_1)
    store_list(read_path_2, collection_2)
    store_list(read_path_3, collection_3)
    store_list(read_path_4, collection_4)
    # 关闭客户端
    client.close()


if __name__ == '__main__':
    main()
