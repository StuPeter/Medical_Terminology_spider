#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/17
# @Author  : 圈圈烃
# @File    : get_medical_from_baidu
# @description:
#
#


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import  DesiredCapabilities
import time

dcap = dict(DesiredCapabilities.PHANTOMJS)      # 将DesiredCapabilities转换为一个字典，方便添加键值对
dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0')
driver = webdriver.PhantomJS(desired_capabilities=dcap)     # 伪装访问
driver.maximize_window()    # 设置全屏
driver.get("https://baike.baidu.com/wikitag/taglist?tagId=75953")
time.sleep(5)
js = 'window.scrollTo(0, 100000);'
driver.execute_script(js)
time.sleep(20)
data = driver.page_source   # 获取网页文本
driver.save_screenshot('Name_Url_data/Html_2.png')   # 截图保存
with open("Name_Url_data/Html_2.txt", 'w') as f:
    f.write(data)
    f.close()
print("Success save")
driver.quit()




# time.sleep(5)
# js = 'window.scrollTo(0, document.body.scrollHeight);'
# driver.execute_script(js)
# time.sleep(5)
# driver.execute_script(js)
# time.sleep(5)
# title = driver.find_element_by_class_name("waterFall_content_title")
# url = driver.find_element_by_xpath("//div[@class='waterFall_item ']/a")
# print(driver.title)
# print(title)
# print(url)

# driver.quit()