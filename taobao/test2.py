# -*- encoding: utf-8 -*-
'''
@File    :   test2.py   
@Contact :   13105350231@163.com
@License :   (C)Copyright 2022-2025
@Desciption : 

@Modify Time      @Author    @Version   
------------      -------    --------   
2023/4/17 9:50   fxk        1.0         
'''
from taobao.util import create_chrome_driver, add_cookies

browser = create_chrome_driver()
browser.get("https://s.taobao.com")
add_cookies(browser, 'taobao.json')
browser.get("https://s.taobao.com")