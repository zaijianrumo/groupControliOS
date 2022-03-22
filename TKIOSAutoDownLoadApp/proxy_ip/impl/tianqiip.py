"""
天启的代理ip
"""
import json

import requests

from TKIOSAutoDownLoadApp.proxy_ip.impl.proxy_ip_interface import ProxyIpAbstract
from TKIOSAutoDownLoadApp.proxy_ip.ip_info import IpInfo


class TianQiIp(ProxyIpAbstract):

    def get_proxy_ip(self, size):
        response = requests.get(
            "http://api.tianqiip.com/getip?secret=9f6mevjzubudr6wr&type=json&num={}&time=3&port=1".format(size))
        text = response.text
        response_ip = json.loads(text)
        if response_ip.get("code") == None or response_ip.get("code") != 1000:
            raise Exception("获取ip失败: {}".format(text))
        ips: list = response_ip.get("data")
        ip_infos = []
        for ip in ips:
            ip_info = IpInfo(ip["ip"], str(ip["port"]), "", "", "")
            ip_infos.append(ip_info)
        return ip_infos
