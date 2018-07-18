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


def get_html(page_num):
    """获取百度百科医疗术语"""
    url = "https://baike.baidu.com/wikitag/api/getlemmas"   # 目标链接
    # proxies = {"https": "http://221.202.72.250:53281", }   # 设置代理
    proxies = {"http": "http://103.109.58.242:8080", }   # 设置代理
    headers = {
        "Host": "baike.baidu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://baike.baidu.com/wikitag/taglist?tagId=75953",
        # "Cookie": "BAIDUID=3DD7B34F9D6150DF0D51021532ED0A8A:FG=1; BIDUPSID=3DD7B34F9D6150DF0D51021532ED0A8A; PSTM=1531732931; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1531798081; pgv_pvi=5285199872; H_PS_PSSID=26524_1469_21088_18559_20928; PSINO=5; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1531814395; pgv_si=s3781830656"
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
    with open("Name_Url_data/medical_json/medical_json(" + str(page_num) + ").txt", 'w') as f:
        f.write(res_json)
        f.close()
    print("Success get json")
    analysis_json("Name_Url_data/medical_json/medical_json(" + str(page_num) + ").txt")


def analysis_json(json_path):
    """解析获取的json数据"""
    # 解析数据
    with open(json_path, "r") as fr:
        med_txt = fr.read()
        med_json = json.loads(med_txt)
    for list_num in range(len(med_json['lemmaList'])):
        med_title = med_json['lemmaList'][list_num]['lemmaTitle']
        med_url = med_json['lemmaList'][list_num]['lemmaUrl']
        # 保存数据
        with open("Name_Url_data/medical_list/medical_list_sum.txt", "a") as fs:
            fs.write(med_title + "---" + med_url + "\n")
    print("Success save list")


def main():
    for i in range (71, 74):
        get_html(page_num=i)


if __name__ == '__main__':
    main()
