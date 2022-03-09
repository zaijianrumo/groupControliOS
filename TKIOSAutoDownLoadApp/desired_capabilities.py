#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from appium import webdriver
from TKIOSAutoDownLoadApp.baseIosPhone import *


def get_desired_capabilities(udid, app, port, lport):
    desired_caps = {
        # 平台名称
        'platformName': "iOS",
        # 平台版本
        'platformVersion': get_ios_version(udid),
        # 设备名称 li的iPhone
        'deviceName': get_ios_product_name(udid),
        # 如果填bundlid会无法调起应用
        'app': app,
        # 设备UDID
        'udid': udid,
        # 是否不重新安装启动
        'noReset': True,
        # 超时时间
        'newCommandTimeout': 600,
        # 自动化测试平台
        'automationName': 'XCUITest',

        "xcodeSigningId": "iPhone Developer",

        'xcodeOrgId': "XH3Y936B53",

        # 'wdaLocalPort': int(lport)
    }
    print('参数:{}'.format(desired_caps))
    remote_url = 'http://127.0.0.1:' + "4723" + '/wd/hub'
    print(remote_url)
    driver = webdriver.Remote(remote_url, desired_caps)
    return driver
