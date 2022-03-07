#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import random
import socket
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor


class tkserver(object):

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

        # 获得端口号

    def getPort(self):
        port = random.randint(4723, 4800)
        # 判断端口是否被占用
        while self.isOpen('127.0.0.1', port):
            port = random.randint(4723, 4800)
        return port

    def runAppiumServer(self, port):
        """启动appium服务
        :return port_list
        """
        print('start appium service')
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        cmd_appium = 'appium -p ' + str(port) + ' --session-override'
        print(cmd_appium)
        try:
            # 启动appium服务
            appiumlog = open(now_time + '_log.txt', 'w')
            subprocess.Popen(cmd_appium, shell=True, stdout=appiumlog)
            print("服务已经启动了")
        except Exception as msg:
            print('error message:', msg)
            raise

        # 分配几个线程池

    executor = ThreadPoolExecutor(6)
    ports = []

    # 启动多个appium服务
    def create_pools(self, device_list_length):
        for i in range(device_list_length):
            port = self.getPort()
            self.ports.append(port)
            self.executor.submit(self.runAppiumServer, port)
        return ('running')

    # 关闭appium服务
    def kill_appium(self):
        cmd_kill = 'pkill node'
        os.system(cmd_kill)
        print('close appium service')
