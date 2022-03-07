#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from appium import webdriver
import time
from concurrent.futures import ThreadPoolExecutor
from TKIOSAutoDownLoadApp.tkserver01  import tkserver


def get_desired_capabilities(udid, wdaport, port):
    desired_caps = {
        # 平台名称
        'platformName': "iOS",
        # 平台版本
        'platformVersion': '13.3',
        # 设备名称 li的iPhone
        'deviceName': 'iPhone 7',
        # 如果填bundlid会无法调起应用
        'app': 'com.ss.iphone.ugc.Aweme',
        'bundleId':'com.ss.iphone.ugc.Aweme',
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

        'wdaLocalPort': wdaport
    }
    remote_url = 'http://localhost:' + "8100" + '/wd/hub'
    print(remote_url)
    drivers = webdriver.Remote(remote_url, desired_caps)
    print("执行到这里了2")
    time.sleep(5)
    print("执行到这里了3")
    drivers.remove_app("com.ss.iphone.ugc.Aweme")
    print("执行到这里了")
    return drivers


def runApp():
    device_list = [('e78cdc38581092179c4b3cfc28ade49cea3a1370', '8001')]
    tks = tkserver()
    tks.create_pools(len(device_list))
    port_list = tks.ports
    time.sleep(2)

    executor = ThreadPoolExecutor(6)
    for i in range(len(device_list)):
        dev = device_list[i][0]
        wdaport = device_list[i][1]
        port = port_list[i]
        driver = executor.submit(get_desired_capabilities, dev, wdaport, port)
