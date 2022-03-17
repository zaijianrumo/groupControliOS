#!/usr/bin/python
# -*- coding: UTF-8 -*-
from appium import webdriver
from TKIOSAutoDownLoadApp.baseConfg.tk_baseIosPhone import *
from selenium.webdriver.common.by import By
import unittest
from openpyxl import load_workbook, Workbook
from TKIOSAutoDownLoadApp.proxy_ip import ProxyIp, IpInfo
import requests
import time

# 操作目标APP
appbundleid = "com.lxkj.youji"


class MyDesiredCapabilities:
    def get_desired_capabilities(self, udid, port, wdaPort):
        desired_caps = {
            # 平台名称
            'platformName': "iOS",
            # 平台版本
            'platformVersion': get_ios_version(udid),
            # 设备名称 li的iPhone
            'deviceName': get_ios_product_name(udid),
            # 如果填bundlid会无法调起应用
            'app': 'com.tk.getIdfa.TKIDFA',
            # 设备UDID
            'udid': udid,
            # 是否不重新安装启动
            'noReset': True,
            'autoAcceptAlerts': True,
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
        iphone_udid = udid
        print(desired_caps)
        remote_url = 'http://localhost:' + str(port) + '/wd/hub'
        print(remote_url)
        driver = webdriver.Remote(remote_url, desired_caps)
        self.startTest(driver)
        return driver

    def startTest(self, driver: webdriver):
        app_is_exited = driver.is_app_installed(appbundleid)
        if app_is_exited:
            # app 存在就删除
            print("目标app存在")
            driver.remove_app(appbundleid)
            print("已删除目标APP重新下载")
            self.downAppTest_01(driver)
        else:
            print("目标APP不存在")
            self.downAppTest_01(driver)

    def downAppTest_01(self, driver: webdriver):

        # httpFiled = driver.find_element(by=By.NAME, value='tk_httpFiled')

        # if len(httpFiled.text) == 0:
        # httpFiled.send_keys("https://apps.apple.com/cn/app/%E6%8A%96%E9%9F%B3/id1142110895")
        idfaLab = driver.find_element(by=By.NAME, value='idfalabIdentifier')
        idfaStr = idfaLab.text

        driver.find_element(by=By.NAME, value="tk_autoDownloadApp").click()

        time.sleep(3)
        driver.find_element(by=By.NAME, value="重新下载").click()
        print("正在下载中,请稍后")
        # 判断app是否存在
        while True:
            time.sleep(2)
            if driver.is_app_installed(appbundleid):
                print("目标APP下载完成")
                break
        driver.background_app(-1)

        proxy_ip = ProxyIp(maxsize=1, threshold=1)
        ip_info: IpInfo = proxy_ip.get_proxy_ip_info()
        ip_address = ip_info.get_ip()
        ip_port = ip_info.get_port()

        # 配置代理
        self.proxyIp_Change(driver, ip_address, ip_port)

        # 打开目标APP
        driver.activate_app(appbundleid)
        time.sleep(3)
        # driver.find_element(by=By.NAME, value="允许").click()
        # time.sleep(1)
        # driver.find_element(by=By.NAME, value="允许一次").click()
        # time.sleep(1)
        #
        # time.sleep(2)
        driver.background_app(-1)
        # 上报
        url = "http://tracking.token-ad.com/gateway/channel?tokenid=3608&subid=0&idfa=%s&ip=%s" % (idfaStr, ip_address)
        r = requests.get(url)
        # 关闭代理
        self.close_proxyIp(driver)

        # 还原广告标识符
        self.reduction_idfa(driver)
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('---------------------------------------------{}'.format(now_time))
        driver.launch_app()
        self.startTest(driver)

    def proxyIp_Change(self, driver: webdriver, ip_address, ip_port):
        print("设置代理IP")
        driver.activate_app('com.apple.Preferences')
        driver.find_element(by=By.NAME, value='无线局域网').click()
        time.sleep(2)
        if driver.capabilities["udid"] == "d6acb3b580c166fc9172ebd5dd2d3f2749ce5c3c":
            driver.find_element(by=By.NAME, value="SZDX_5G, 安全网络, 信号强度 3 格，共 3 格").click()
        else:
            driver.find_element(by=By.NAME, value="SZDX_5G, 安全网络, 信号强度3格，共3格").click()
        driver.execute_script('mobile: swipe', {'direction': 'up'})
        driver.find_element(by=By.NAME, value='配置代理').click()
        driver.find_element(by=By.NAME, value='手动').click()
        addressFiled = driver.find_element(by=By.NAME, value="服务器")
        addressFiled.clear()
        addressFiled.send_keys(ip_address)
        time.sleep(1)
        porTFiled = driver.find_element(by=By.NAME, value="端口")
        porTFiled.clear()
        porTFiled.send_keys(ip_port)
        driver.find_element(by=By.NAME, value="存储").click()
        time.sleep(1)
        driver.background_app(-1)
        driver.terminate_app('com.apple.Preferences')

    def close_proxyIp(self, driver: webdriver):
        print("关闭代理IP")
        driver.activate_app('com.apple.Preferences')
        driver.find_element(by=By.NAME, value='无线局域网').click()
        time.sleep(2)
        if driver.capabilities["udid"] == "d6acb3b580c166fc9172ebd5dd2d3f2749ce5c3c":
            driver.find_element(by=By.NAME, value="SZDX_5G, 安全网络, 信号强度 3 格，共 3 格").click()
        else:
            driver.find_element(by=By.NAME, value="SZDX_5G, 安全网络, 信号强度3格，共3格").click()
        driver.execute_script('mobile: swipe', {'direction': 'up'})
        driver.find_element(by=By.NAME, value='配置代理').click()
        driver.find_element(by=By.NAME, value='关闭').click()
        driver.find_element(by=By.NAME, value="存储").click()
        time.sleep(1)
        driver.back()
        time.sleep(1)
        driver.back()
        time.sleep(1)
        driver.back()

    # 还原广告标识符
    def reduction_idfa(self, driver: webdriver):
        # 隐私
        driver.execute_script('mobile: swipe', {'direction': 'up'})
        driver.find_element(by=By.NAME, value='隐私').click()
        driver.execute_script('mobile: swipe', {'direction': 'up'})
        driver.find_element(by=By.NAME, value='广告').click()
        driver.find_element(by=By.NAME, value='还原广告标识符…').click()
        time.sleep(1)
        # 允许弹框
        driver.switch_to.alert.accept()
        time.sleep(1)
        driver.terminate_app('com.apple.Preferences')
        driver.background_app(-1)
