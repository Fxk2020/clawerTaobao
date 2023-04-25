# -*- encoding: utf-8 -*-
'''
@File    :   Demo20.py   
@Contact :   13105350231@163.com
@License :   (C)Copyright 2022-2025
@Desciption : 模拟淘宝用户登录

@Modify Time      @Author    @Version   
------------      -------    --------   
2023/4/6 20:39   fxk        1.0         
'''
import json

from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

# 初始
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from settings import WEBDRIVER_PATH, USER_NAME, USER_PASSWORD


def loginInTaobao(username, userpassword):
    bro = webdriver.Chrome(executable_path=WEBDRIVER_PATH)
    option = Options()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option("detach", True)
    script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
    bro.execute_script(script)
    bro.maximize_window()

    bro.get("https://login.taobao.com/member/login.jhtml")
    time.sleep(1)

    bro.find_element_by_name("fm-login-id").send_keys(username)
    time.sleep(1)
    bro.find_element_by_name("fm-login-password").send_keys(userpassword)
    time.sleep(1.5)

    SwitchFrame(bro)
    time.sleep(2)
    bro.switch_to.window(bro.window_handles[0])
    # 登录
    bro.find_element_by_xpath("//*[@id='login-form']/div[4]/button").click()
    time.sleep(2)
    # 可能是淘宝的反爬机制，需要再一次滑动滑块
    SwitchFrame(bro)

    time.sleep(5)
    with open('taobao.json', 'w') as file:
        json.dump(bro.get_cookies(), file)
    # bro.quit()  # 关闭浏览器


# 获取
def SwitchFrame(bro):
    """
    需要进入frame中进行处理
    :param bro:
    :return:
    """
    bro.switch_to.frame('baxia-dialog-content')
    js = 'Object.defineProperty(navigator,"webdriver",{get:()=>false,});'
    bro.execute_script(js)
    huakuai = WebDriverWait(bro, 100).until(
        EC.presence_of_element_located((By.ID, 'nc_1_n1z')))

    # 动作链
    newaction = ActionChains(driver=bro)
    newaction.move_to_element(huakuai)
    newaction.click_and_hold(huakuai)
    newaction.move_by_offset(300, 0).perform()
    # for i in range(3):
    #     newaction.move_by_offset(100, 0).perform()
    #     time.sleep(0.5)
    newaction.release()


if __name__ == "__main__":
    loginInTaobao(USER_NAME, USER_PASSWORD)

