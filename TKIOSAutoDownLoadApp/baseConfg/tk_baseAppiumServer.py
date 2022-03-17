# -*- coding: utf-8 -*-

import os
from multiprocessing import Process
import subprocess
import multiprocessing
from time import ctime
from time import sleep
import time
import platform

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class AppiumServer:
    def __init__(self, kwargs=None):
        self.kwargs = kwargs
        # 干掉所有appium 服务
        cmd_appium = "killall - 9 node"
        subprocess.Popen(cmd_appium, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         close_fds=True)
        time.sleep(1)
    appium_process = []  # 进程组

    def start_server(self):
        """ start the appium server
        """
        for i in range(0, len(self.kwargs)):
            port = self.kwargs[i]["port"]
            bport = self.kwargs[i]["wdaPort"]
            udid = self.kwargs[i]["udid"]
            appium = multiprocessing.Process(target=self.runAppiumServer(port, bport, udid))
            self.appium_process.append(appium)
        for appium in self.appium_process:
            appium.start()

        for appium in self.appium_process:
            appium.join()

    def runAppiumServer(self, port: str, bport: str, udid: str):
        """ start the appium server
        """
        cmd_appium = "appium -a 127.0.0.1 -p %s -U %s --log ./serverlogs/%s.log  --session-override" % (
            port, udid, udid)
        appium = subprocess.Popen(cmd_appium, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  close_fds=True)
        print(cmd_appium)
        time.sleep(1)

    def stop_server(self, devices: list):
        sysstr = platform.system()
        if sysstr == 'Windows':
            os.popen("taskkill /f /im node.exe")
        else:
            for device in devices:
                cmd = "lsof -i :{0}".format(device)
                plist = os.popen(cmd).readlines()
                plisttmp = plist[1].split("    ")
                plists = plisttmp[1].split(" ")
                os.popen("kill -9 {0}".format(plists[0]))
