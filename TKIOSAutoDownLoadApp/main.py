# -*- coding: utf-8 -*-

import sys
import random
import unittest
from TKIOSAutoDownLoadApp.baseIosPhone import *
from multiprocessing import Pool
from TKIOSAutoDownLoadApp.baseAppiumServer import *
from datetime import datetime
from appium import webdriver
from TKIOSAutoDownLoadApp.desired_capabilities import get_desired_capabilities


def runnerPool(getDevices):
    for i in range(0, len(getDevices)):
        udid = getDevices[i]['devices']
        app = getDevices[i]["app"]
        port = getDevices[i]["port"]
        driver = executor.submit(get_desired_capabilities(udid, app, str(port)))


def runnerCaseApp(devicess):
    suite = unittest.TestSuite()
    suite.addTest(mainAppTest_01())
    unittest.TextTestRunner(verbosity=2).run(suite)


def mainAppTest_01(self):
    pass


executor = ThreadPoolExecutor(6)
if __name__ == '__main__':
    devicess = get_ios_devices()
    print(devicess)
    if len(devicess) > 0:
        l_devices = []
        for dev in devicess:
            app = {}
            app["devices"] = dev
            app["port"] = ServerValidation().getPort()
            app["bport"] = ServerValidation().getPort()
            app["app"] = "com.apple.AppStore"
            l_devices.append(app)
        appium_server = AppiumServer(l_devices)
        appium_server.start_server()
        time.sleep(5)
        runnerPool(l_devices)
