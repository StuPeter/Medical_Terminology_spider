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
            # print('文件名：%s' % filename)
            # print('文件完整路径：%s\n' % file_path)


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
    try :
        content = soup.find_all(attrs={"name": "description"})[0]['content']
        doc = {
            "名称": filename,
            "简介": content.replace("...", "")
        }
    except:
        doc = {
            "名称": filename,
            "简介": None,
        }
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
            # print(value_list)
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
            except:
                break


        # print(value_list)
        value_new_list = ""
        for j in range(len(value_list)):
            value_new_list += value_list[j]
        # print(value_new_list)
        value_lists.append(value_new_list)

    # print(len(value_lists) == len(key_lists))

    for i in range(len(key_lists)):
        doc[key_lists[i]] = value_lists[i]
    # print(doc)
    collection.insert_one(doc)
    # print("保存成功")


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
            except:
                print("第" + str(count) + "个页面无法存入数据库！！！>>>>>>>>>>>>>>>%.2f%%" % (count / len(filenames) * 100))
                count += 1



def main():

    read_path_1 = "Name_Url_data\\drug_html"
    read_path_2 = "Name_Url_data\\diagnosis_html"
    read_path_3 = "Name_Url_data\\chinese_medicine_html"
    read_path_4 = "Name_Url_data\\disease_html"
    # # 连接MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    # # 获取名字为 medical_db 的数据库对象
    db = client.medical_detial_db
    # # 获取名字为 disease
    collection_1 = db.drug
    collection_2 = db.diagnosis
    collection_3 = db.chinese_medicine
    collection_4 = db.disease
    # # 存入数据
    # store_list_detial(read_path_1, collection_1)
    # store_list_detial(read_path_2, collection_2)
    store_list_detial(read_path_3, collection_3)
    store_list_detial(read_path_4, collection_4)
    # # 关闭客户端
    client.close()
    """
    read_path = "Name_Url_data\\drug_html"
    store_list_detial(read_path)
    """


if __name__ == '__main__':
    main()
