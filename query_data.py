#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/27
# @Author  : 圈圈烃
# @File    : query_data
# @description: 查询数据
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
    collection_1 = db.drug
    collection_2 = db.diagnosis
    collection_3 = db.chinese_medicine
    collection_4 = db.disease
    # 模糊查询
    for need in collection_1.find({'名称': re.compile("痛")}):
        print(type(need))


if __name__ == '__main__':
    main()

