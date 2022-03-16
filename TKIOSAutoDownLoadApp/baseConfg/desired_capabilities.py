#!/usr/bin/python
# -*- coding: UTF-8 -*-
from appium import webdriver
from TKIOSAutoDownLoadApp.baseConfg.baseIosPhone import *
import unittest

globals
drivers = []


class MyDesiredCapabilities(unittest.TestCase):
    def get_desired_capabilities(self, udid, port, wdaPort):
        desired_caps = {
            # 平台名称
            'platformName': "iOS",
            # 平台版本
            'platformVersion': get_ios_version(udid),
            # 设备名称 li的iPhone
            'deviceName': get_ios_product_name(udid),
            # 如果填bundlid会无法调起应用
            'app': 'com.apple.AppStore',
            # 设备UDID
            'udid': udid,
            # 是否不重新安装启动
            'noReset': True,
            # 超时时间
            'newCommandTimeout': 600,
            # 自动化测试平台
            'automationName': 'XCUITest',
            # "xcodeSigningId": "iPhone Developer",
            # 'xcodeOrgId': "XH3Y936B53",
            'autoLaunch': True,
            'clearSystemFiles': True,
            # 'showIOSLog': True,
            'wdaLocalPort': wdaPort

        }
        print(desired_caps)
        remote_url = 'http://localhost:' + str(port) + '/wd/hub'
        print(remote_url)
        self.driver = webdriver.Remote(remote_url, desired_caps)
        self.driver.background_app(-1)
        self.driver.quit()
        return self.driver
