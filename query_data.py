#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/27
# @Author  : 圈圈烃
# @File    : query_data
# @Description: 查询数据
#
#
from pymongo import MongoClient
import re


def main():
    # 连接MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    # 获取名字为 medical_db 的数据库对象
    db = client.medical_detial_db
    # 获取名字为 disease
    collection_1 = db.disease
    collection_2 = db.drug
    collection_3 = db.diagnosis
    collection_4 = db.chinese_medicine
    # 模糊查询
    key_word = input("请输入关键词进行查询：")
    count = collection_1.find({'名称': re.compile(key_word)}).count()
    print("以下一共为你查询到" + str(count) + "条数据")
    for need in collection_1.find({'名称': re.compile(key_word)}):
        print(need)


if __name__ == '__main__':
    main()

