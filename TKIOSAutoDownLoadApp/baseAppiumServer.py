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
import multiprocessing

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

    appium_process = []  # 进程组

    def start_server(self):
        """ start the appium server
        """
        for i in range(0, len(self.kwargs)):
            port = self.kwargs[i]["port"]
            bport = self.kwargs[i]["bport"]
            udid = self.kwargs[i]["devices"]
            appium = multiprocessing.Process(target=self.runAppiumServer(port, bport, udid))
            self.appium_process.append(appium)
        for appium in self.appium_process:
            appium.start()

        for appium in self.appium_process:
            appium.join()

    def runAppiumServer(self, port: str, bport: str, udid: str):
        """ start the appium server
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # cmd_appium = "appium --session-override  -p %s --webdriveragent-port %s -U %s" % (
        # port, bport, udid)
        # cmd_appium = "appium --session-override  -p %s -U %s" % (
        #     port, udid)
        cmd_appium = "appium"
        print(cmd_appium)
        # try:
        #     # 启动appium服务
        #     subprocess.Popen(cmd_appium, shell=True, stdout=open('../logs/' + now_time + udid + 'log.txt', 'a'),
        #                      stderr=subprocess.STDOUT)
        #     print("服务已经启动了")
        # except Exception as msg:
        #     print('error message:', msg)
        #     raise

        appium = subprocess.Popen(cmd_appium, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  close_fds=True)
        try:
            while True:
                appium_line = appium.stdout.readline().strip().decode()
                print("---------start_server----------")
                if 'Welcome to Appium' in appium_line or 'Error: listen' in appium_line:
                    print("----server启动成功---")
                    break
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
