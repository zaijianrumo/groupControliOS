# -*- coding: utf-8 -*-
import socket
import random
import urllib.request
from urllib.error import URLError

# 端口验证
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
