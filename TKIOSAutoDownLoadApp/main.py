# -*- coding: UTF-8 -*-
# from tkinter.tix import Shell

from tkinter.tix import Shell
from appium import webdriver

from TKIOSAutoDownLoadApp import desired_capabilities
from time import sleep
import unittest
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler
from TKIOSAutoDownLoadApp.tkserver01 import tkserver
import time

scheduler = BlockingScheduler()
appbundleid = "com.ss.iphone.ugc.Aweme"


class TKIOSDownLoadTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        desired_capabilities.runApp()

    @classmethod
    def tearDownClass(self):
        pass

    def downAppTest_01(self):
        # 点击 '搜索' item
        searchBtn = self.driver.find_element(by=By.XPATH, value='//XCUIElementTypeButton[@name="搜索"]')
        searchBtn.click()

        # 获取搜索框
        searchTexFiled = self.driver.find_element(by=By.XPATH,
                                                  value='//XCUIElementTypeSearchField[@name="游戏、App、故事以及更多"]')
        searchTexFiled.send_keys("抖音")
        # 这句代码可以解决搜索问题
        searchTexFiled.send_keys("\n")

        sleep(2)
        # downCellBtn = self.driver.find_element(by=By.XPATH,value='xpath//XCUIElementTypeCell[@name="抖音, 记录美好生活, 四又四分之三颗星, 3774万个评分"]').click()
        downDetailBtn = self.driver.find_element(by=By.XPATH, value='//XCUIElementTypeButton[@name="重新下载"]').click()
        print("开始下载")

        # scheduler.add_job(self.downingTest_01, 'interval', seconds=2)
        # scheduler.start()

        status = self.driver.query_app_stat(appbundleid)
        print(status)

    def downingTest_01(self):
        appIsExited = self.driver.is_app_installed(appbundleid)
        if appIsExited:
            print("下载完成........")
            # 移除定时器
            scheduler.remove_all_jobs()
            sleep(2)
            self.driver.remove_app(appbundleid)
            self.downAppTest_01()

    def mainAppTest_01(self):
        pass
        # sleep(10)
        # appIsExited = self.driver.is_app_installed(appbundleid)
        # if appIsExited:
        #    #app 存在就删除
        #    print("目标app存在")
        #    self.driver.remove_app(appbundleid)
        #    sleep(1)
        #    self.downAppTest_01()
        # else:
        #    print("目标APP不存在")
        #    self.downAppTest_01()


if __name__ == '__main__':
    suit = unittest.TestSuite()
    suit.addTest(TKIOSDownLoadTest('mainAppTest_01'))
    unittest.TextTestRunner(verbosity=2).run(suit)
