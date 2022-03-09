# -*- coding: utf-8 -*-

import os
import socket
import urllib.request
from urllib.error import URLError
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
import time
import random
import time
import platform
import subprocess

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
import threading


class ServerValidation:
    # 判断端口是否被占用
    def isOpen(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip), int(port))
            # shutdown参数表示后续可否读写
            s.shutdown(2)
            print('%d is used' % port)
            return True
        except Exception:
            print('%d is available' % port)
            return False

    def getPort(self):
        port = random.randint(4700, 4900)
        # 判断端口是否被占用
        while self.isOpen('127.0.0.1', port):

            port = random.randint(4700, 4900)
        return port


class AppiumServer:

    def __init__(self, kwargs=None):
        self.kwargs = kwargs

    executor = ThreadPoolExecutor(6)

    def start_server(self):
        """ start the appium server
        """
        for i in range(0, len(self.kwargs)):
            self.executor.submit(self.runAppiumServer(self.kwargs[i]["port"], self.kwargs[i]["bport"],
                                                      self.kwargs[i]["devices"]))

    def runAppiumServer(self, port: str, bport: str, udid: str):
        """ start the appium server
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cmd_appium = "appium --session-override  -p %s --webdriveragent-port %s --device-name %s" % (
            port, bport, udid)
        appiumlog = open(now_time + udid + 'log.txt', 'w')
        try:
            # 启动appium服务
            subprocess.Popen(cmd_appium, shell=True, stdout=appiumlog)
            print("服务已经启动了")
        except Exception as msg:
            print('error message:', msg)
            raise

    def stop_server(self, devices):
        sysstr = platform.system()
        if sysstr == 'Windows':
            os.popen("taskkill /f /im node.exe")
        else:
            for device in devices:
                # mac
                cmd = "lsof -i :{0}".format(device["port"])
                plist = os.popen(cmd).readlines()
                plisttmp = plist[1].split("    ")
                plists = plisttmp[1].split(" ")
                os.popen("kill -9 {0}".format(plists[0]))

    def re_start_server(self):
        """reStart the appium s
        """
        # self.stop_server()
        # self.start_server()
        pass
