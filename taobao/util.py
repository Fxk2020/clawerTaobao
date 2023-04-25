# -*- encoding: utf-8 -*-
'''
@File    :   util.py   
@Contact :   13105350231@163.com
@License :   (C)Copyright 2022-2025
@Desciption : 

@Modify Time      @Author    @Version   
------------      -------    --------   
2023/4/17 9:47   fxk        1.0         
'''
import json
import re

from selenium import webdriver
from taobao.settings import WEBDRIVER_PATH


def create_chrome_driver(*, headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=options,
                               executable_path=WEBDRIVER_PATH)
    browser.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator,"webdriver",{get: () => undefined}'}
    )
    return browser


def add_cookies(browser, cookie_file):
    with open(cookie_file, 'r') as file:
        cookies_list = json.load(file)
        for cookie_dict in cookies_list:
            if cookie_dict['secure']:
                browser.add_cookie(cookie_dict)


def re_font(text):
    """
    去除其他字符
    :param text:
    :return:
    """
    text = text.replace("\n", "")
    pattern = re.compile('[^a-zA-Z ]+')
    return pattern.findall(text)[0]


def read_keywords(file):
    with open(file, "r", encoding='utf-8') as f:
        data = f.readlines()
    keywords = []
    for i in data:
        i = i.replace("\n", "")
        keywords.append(i)
    # print(keywords)
    return keywords


# keywords = read_keywords("C:\\Users\\yuanbao\\Desktop\\taobao\\taobao\\keywords.txt")
# for i in keywords:
#     print(i)

# pages = 100
# page = 0
# while page < pages:
#     print(page)
#     page = page+1
#     if page == 7:
#         pages = 10
#         print(f'ffffffffffffffffffffffffff{pages}')