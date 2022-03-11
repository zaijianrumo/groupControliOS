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

    appium_process = []  # 进程组

    def start_server(self):
        """ start the appium server
        """
        for i in range(0, len(self.kwargs)):
            port = self.kwargs[i]["port"]
            bport = self.kwargs[i]["bport"]
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
        cmd_appium = f"appium -p %s -U %s --log ./serverlogs/%s.log --session-override" % (
            port, udid, udid)
        print(cmd_appium)
        appium = subprocess.Popen(cmd_appium, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  close_fds=True)
        try:
            while True:
                appium_line = appium.stdout.readline().strip().decode()
                if 'listener started' in appium_line or 'Error: listen' in appium_line:
                    print("----server启动成功---")
                    break
        except Exception as msg:
            print('error message:', msg)
            raise


def stop_server(devices: list):
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
