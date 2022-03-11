# -*- coding: utf-8 -*-

import sys
import random
import subprocess
import multiprocessing
import time
import unittest
from TKIOSAutoDownLoadApp.baseAppiumServer import *
from TKIOSAutoDownLoadApp.portVerify import *
from TKIOSAutoDownLoadApp.desired_capabilities import *
from TKIOSAutoDownLoadApp.baseIosPhone import *
from appium import webdriver

# 构建desired进程组
desired_process = []


def runnerPool(getDevices):
    for i in range(0, len(getDevices)):
        udid = getDevices[i]['udid']
        port = getDevices[i]["port"]
        bport = getDevices[i]["bport"]
        desired = multiprocessing.Process(target=MyDesiredCapabilities().get_desired_capabilities,
                                          args=(udid, str(port), str(bport)))
        # desired = multiprocessing.Process(
        #     target=MyDesiredCapabilities().get_desired_capabilities(udid, str(port), bport))
        desired_process.append(desired)
        # 启动多设备执行测试
    for desired in desired_process:
        desired.start()
        # 等所有进程结束后关闭
    for desired in desired_process:
        desired.join()


def runnerCaseApp(devicess):
    suite = unittest.TestSuite()
    suite.addTest(mainAppTest_01())
    unittest.TextTestRunner(verbosity=2).run(suite)


def mainAppTest_01(self):
    pass


if __name__ == '__main__':
    # 获取设备的UDID
    devicess = get_ios_devices()
    print(devicess)
    if len(devicess) > 0:
        l_devices = []
        int
        i = 0
        for dev in devicess:
            i = i + 1
            app = {}
            app["udid"] = dev
            app["port"] = ServerValidation().getPort()
            app["bport"] = ServerValidation().getPort()
            l_devices.append(app)
        appium_server = AppiumServer(l_devices)
        appium_server.start_server()
        runnerPool(l_devices)
