#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/18
# @Author  : 圈圈烃
# @File    : get_ip
# @description: 建立IP池
#
#


from bs4 import BeautifulSoup
import requests
import re
import time


def get_html(url, ip=False, ip_proxies=None):
    """
    获取网页
    :param url:链接
    :param ip: 是否开启代理，Ture，False
    :param ip_proxies: 代理地址
    :return:
    """
    try:
        pattern = re.compile(r'//(.*?)/')
        Host_url = pattern.findall(url)[0]
        headers = {
            "Host": Host_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        # proxies = {"http": "http://103.109.58.242:8080", }   # 设置代理
        if ip:
            proxies = {"http": "http://" + ip_proxies, }  # 设置代理
            res = requests.get(url, headers=headers, proxies=proxies, timeout=5)
        else:
            res = requests.get(url, headers=headers, timeout=5)
        res.encoding = res.apparent_encoding
        print("Html页面获取成功 " + url)
        return res.text
    except:
        print("Html页面获取失败 " + url)


def save_ip(data, save_path):
    """
    保存ip信息到txt
    :param data: 数据类型为列表
    :return:
    """
    try:
        print("总共获取 " + str(len(data)) + " 条数据")
        with open(save_path, "a") as f:
            for i in range(len(data)):
                f.write(data[i])
            f.close()
            print("IP池文件保存成功")
    except:
        print("IP池文件保存失败")


def check_ip(path):
    """
    ip 查重
    :param path: file path
    :return:
    """
    try:
        # 读取文件查重
        data_list = []
        with open(path, "r") as fr:
            lines = fr.readlines()
            fr.close()
        for line in lines:
            data_list.append(line)
        new_data_list = list(set(data_list))    # 查重
        # print(data_list)
        file_name = path.split("/")
        print(file_name[-1] + "文件共有 " + str(len(data_list)) + " 条数据")
        print("经过查重,现共有 " + str(len(new_data_list)) + " 条数据")
        # 保存文件
        with open(path, "w") as f:
            for i in range(len(new_data_list)):
                f.write(new_data_list[i])
            f.close()
            print("IP池查重成功")
    except:
        print("IP池查重失败")


def ip_format(read_path, save_path):
    """
    将搜集的ip进行格式化转换，二次查重
    :param read_path: 读取待转换的ip的文件路径
    :param save_path: 转换完成的ip的保存路径
    :return:
    """
    data_list = []
    with open(read_path, "r") as fr:
        lines = fr.readlines()
        fr.close()
    for line in lines:
        new_line = line.split("___")
        ip_format_line = new_line[0].replace(" ", "") + ":" + new_line[1] + "\n"
        # print(ip_format_line)
        data_list.append(ip_format_line)
    with open(save_path, "a") as fs:
        for i in range(len(data_list)):
            fs.write(data_list[i])
        fs.close()
        print("格式化IP池保存成功")
        fs.close()


def ip_test(ip_proxies):
    """
    ip可用性验证
    :param ip_proxies: 待测ip：例如：101.96.10.36:88
    :return:
    """
    url = "http://ip.chinaz.com/"
    headers = {
        "Host": "ip.chinaz.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://blog.csdn.net/Winterto1990/article/details/51220307",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }

    proxies = {"http": "http://" + ip_proxies, }   # 设置代理
    res = requests.get(url, headers=headers, proxies=proxies, timeout=2)
    # 解析网页
    soup = BeautifulSoup(res.text, "html.parser")
    info_list = soup.find_all("p", {"class": "getlist pl10"})
    for info in info_list:
        is_local = info.get_text()
        # print(is_local.find("122.244.227.47"))
        print(info.get_text())
    return is_local.find("122.244.227.47")  # 判断是否为本地的地址


def ip_batch_inspection(read_path, save_path):
    """
    ip批量检测
    :param read_path: ip池文件路径
    :param save_path: 可用ip保存路径
    :return:
    """
    with open(read_path, "r") as fr:
        lines = fr.readlines()
        fr.close()
        count = 0
        file_name = read_path.split("/")
        print(file_name[-1] + "文件共有 " + str(len(lines)) + " 条数据")
        for line in lines:
            count += 1
            ip_proxies = line.replace("\n", "")
            try:
                is_local = ip_test(ip_proxies)
                if is_local < 0:
                    with open(save_path, "a") as fs:
                        fs.write(ip_proxies + "\n")
            except:
                pass
                # print("ip不可用")
            print("验证中......%.2f%%" %(count/len(lines)*100))
        print("验证完毕")


def get_data5u_free_ip(ip_pro, save_path):
    """
    爬取无忧代理的免费ip
    :param ip_pro: 要使用的代理ip（这里是用代理ip去爬代理ip）
    :param save_path: 保存路径
    :return:
    """
    url_list = [
        "http://www.data5u.com/free/index.shtml",
        "http://www.data5u.com/free/gngn/index.shtml",
        "http://www.data5u.com/free/gnpt/index.shtml",
        "http://www.data5u.com/free/gwgn/index.shtml",
        "http://www.data5u.com/free/gwpt/index.shtml"
    ]
    ip_list_sum = []

    for i in range(5):
        res_text = get_html(url_list[i], ip=True, ip_proxies=ip_pro)
        # 抓取错误页面，主动报异常
        if (res_text.find("错误") != -1):
            raise AttributeError('错误页面')
        # 页面解析
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find_all("ul", class_="l2")
        for tag in tags:
            ip_list = []
            ip_info_format = ""
            sps = tag.find_all("li")
            for sp in sps:
                ip_info = sp.get_text()
                ip_list.append(ip_info)
            for j in range(len(sps)):
                # 格式化IP信息
                if j == len(sps) - 1:
                    ip_info_format += str(ip_list[j]) + "\n"
                else:
                    ip_info_format += str(ip_list[j]) + "___"
            ip_list_sum.append(ip_info_format)
    # print(ip_list_sum)
    save_ip(ip_list_sum, save_path)


def get_kuaidaili_free_ip(ip_pro, save_path):
    """
    爬取快代理的免费ip
    :param ip_pro: 要使用的代理ip（这里是用代理ip去爬代理ip）
    :param save_path: 保存路径
    :return:
    """
    url_list = "https://www.kuaidaili.com/ops/proxylist/1/"
    ip_list_sum = []

    for i in range(10):  # 获取页数
        res_text = get_html("https://www.kuaidaili.com/ops/proxylist/" + str(i+1) + "/", ip=True, ip_proxies=ip_pro)
        # 页面解析
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find_all("div", id="freelist")
        for tag in tags:
            ip_list = []
            sps = tag.find_all("td")
            # print(tag)
            for sp in sps:
                ip_info = sp.get_text()
                ip_list.append(ip_info)
            # print(ip_list)
            for j in range(10):     # 每页100条数据
                ip_info_format = ""
                for k in range(8):   # 每条6个内容
                    if k == 7:
                        ip_info_format += str(ip_list[(j * 8 + k)]) + "\n"
                    else:
                        ip_info_format += str(ip_list[(j * 8 + k)]) + "___"
                # print(ip_info_format)
                ip_list_sum.append(ip_info_format)
    # print(len(ip_list_sum))
    save_ip(ip_list_sum, save_path)


def get_xsdaili_free_ip(ip_pro, save_path):
    """
    爬取小舒代理的免费ip
    :param ip_pro: 要使用的代理ip（这里是用代理ip去爬代理ip）
    :param save_path: 保存路径
    :return:
    """
    url = "http://www.xsdaili.com/"
    url_list = []
    home_page = get_html(url, ip=True, ip_proxies=ip_pro)
    # 页面解析
    home_soup = BeautifulSoup(home_page, "html.parser")
    home_tags = home_soup.find_all("div", class_="title")
    for home_tag in home_tags:
        home_url = home_tag.a["href"]
        new_url = "http://www.xsdaili.com" + str(home_url)
        url_list.append(new_url)
    # print(url_list)
    ip_list_sum = []
    for i in range(len(url_list)):  # 页面页数
        res_text = get_html(url_list[i], ip=True, ip_proxies=ip_pro)
        # 页面解析
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find("div", class_="cont")
        ip_info = tags.get_text()
        ip_info_temp = ip_info.replace("\r\n\t\t\t\t\t\t\t", "")
        ip_list = re.split(r'[:@# \] ]', ip_info_temp)      # 分割字符串
        for j in range(100):    # 每页100条数据
            ip_info_format = ""
            for k in range(6):  # 每条6个内容
                if k == 5:
                    ip_info_format += str(ip_list[(j * 6 + k)]) + "\n"
                else:
                    ip_info_format += str(ip_list[(j * 6 + k)]) + "___"
            # print(ip_info_format)
            ip_list_sum.append(ip_info_format)
    # print(len(ip_list_sum))
    save_ip(ip_list_sum, save_path)


def get_xicidaili_free_ip(ip_pro, save_path):
    """
    爬取西刺代理的免费ip
    :param ip_pro: 要使用的代理ip（这里是用代理ip去爬代理ip）
    :param save_path: 保存路径
    :return:
    """
    ip_list_sum = []
    for i in range(10):  # 获取页数
        res_text = get_html("http://www.xicidaili.com/nn/" + str(i+1), ip=True, ip_proxies=ip_pro)
        # 抓取错误页面，主动报异常
        # print(res_text)
        if (res_text.find("错误") != -1):     # 错误页面
            raise AttributeError('错误页面')
        elif (res_text == "block"):               # 空白页面
            raise AttributeError('错误页面')
        # 页面解析
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find_all("tr", class_="")
        for tag in tags:
            ip_list = []
            ip_ths = tag.find_all("td")
            for ip_th in ip_ths:
                ip_info = ip_th.get_text().replace("\n", "")
                if ip_info != "":
                    ip_list.append(ip_info)
            # print(ip_list)
            try:
                ip_info_format = ""
                for k in range(7):   # 每条6个内容
                    if k == 6:
                        ip_info_format += str(ip_list[k]) + "\n"
                    else:
                        ip_info_format += str(ip_list[k]) + "___"
                # print(ip_info_format)
                ip_list_sum.append(ip_info_format)
            except:
                pass
    # print((ip_list_sum))
    save_ip(ip_list_sum, save_path)


def get_89ip_free_ip(ip_pro, save_path):
    """
    爬取89免费代理的免费ip
    :param ip_pro: 要使用的代理ip（这里是用代理ip去爬代理ip）
    :param save_path: 保存路径
    :return:
    """
    ip_list_sum = []
    for i in range(10):  # 获取页数
        res_text = get_html("http://www.89ip.cn/index_" + str(i+1) + ".html", ip=True, ip_proxies=ip_pro)
        # 抓取错误页面，主动报异常
        if (res_text.find("错误") != -1):     # 错误页面
            raise AttributeError('错误页面')
        # 页面解析
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find_all("tbody")
        for tag in tags:
            ip_ths = tag.find_all("tr")
            for ip_th in ip_ths:
                ip_tds = ip_th.find_all("td")
                ip_list = []
                for ip_td in ip_tds:
                    ip_info = re.split(r'[\t\n ]', ip_td.get_text())  # 分割字符串
                    for j in range(len(ip_info)):
                        if ip_info[j] != "":
                            ip_list.append(ip_info[j])
                # print(ip_list)
                ip_info_format = ""
                for k in range(len(ip_list)):  # 每条6个内容
                    if k == len(ip_list) - 1:
                        ip_info_format += str(ip_list[k]) + "\n"
                    else:
                        ip_info_format += str(ip_list[k]) + "___"
                # print(ip_info_format)
                ip_list_sum.append(ip_info_format)
    # print(ip_list_sum)
    save_ip(ip_list_sum, save_path)


def main():
    """
    available_ip_path = "Ip_Pools/ip_use_6.txt"  # 目前可用ip地址
    strtime = time.strftime("%Y_%m_%d")     # 当前日期
    ip_pools_path = "Ip_Pools/" + strtime + "_ip_pools.txt"     # 原始ip池地址
    ip_format_pools_path = "Ip_Pools/" + strtime + "_ip_format_pools.txt"   # 格式化后ip池地址
    ip_use_path = "Ip_Pools/" + strtime + "_ip_use.txt"
    ip_use_list = []
    # 读取可用ip地址，爬取ip地址
    with open(available_ip_path, "r") as fr:
        ip_use_lines = fr.readlines()
        for ip_use_line in ip_use_lines:
            ip_use_line_new = ip_use_line.replace("\n", "")
            ip_use_list.append(ip_use_line_new)
    for i in range(len(ip_use_list)):
        # 获取ip建立IP池
        try:
            get_data5u_free_ip(ip_use_list[i], ip_pools_path)
            break
        except:
            pass
    for i in range(len(ip_use_list)):
        # 获取ip建立IP池
        try:
            get_kuaidaili_free_ip(ip_use_list[i], ip_pools_path)
            break
        except:
            pass
    for i in range(len(ip_use_list)):
        # 获取ip建立IP池
        try:
            get_xsdaili_free_ip(ip_use_list[i], ip_pools_path)
            break
        except:
            pass
    for i in range(len(ip_use_list)):
        # 获取ip建立IP池
        try:
            get_xicidaili_free_ip(ip_use_list[i], ip_pools_path)
            break
        except:
            pass
    for i in range(len(ip_use_list)):
        # 获取ip建立IP池
        try:
            get_89ip_free_ip(ip_use_list[i], ip_pools_path)
            break
        except:
            pass
    # 筛选ip进行查重
    ip_format(ip_pools_path, ip_format_pools_path)
    check_ip(ip_format_pools_path)
    # 验证ip可用性
    ip_batch_inspection(ip_format_pools_path, ip_use_path)
"""
    # ip_batch_inspection("Ip_Pools/ip_use_6.txt", "Ip_Pools/ip_use_7.txt")
    check_ip("Ip_Pools/ip_use_7.txt")


if __name__ == '__main__':
    main()