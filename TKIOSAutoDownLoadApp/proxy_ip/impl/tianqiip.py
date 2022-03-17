"""
天启的代理ip
"""
import requests

from TKIOSAutoDownLoadApp.proxy_ip.impl.proxy_ip_interface import ProxyIpAbstract
from TKIOSAutoDownLoadApp.proxy_ip.ip_info import IpInfo

class TianQiIp(ProxyIpAbstract):

    def get_proxy_ip(self, size):
        response = requests.get(
            "http://api.tianqiip.com/getip?secret=9f6mevjzubudr6wr&type=txt&num={}&time=3&port=1".format(size))
        text = response.text
        ip_list = text.split('\r\n')
        ip_list.remove("")  # 去除最后一个""
        ip_infos = []
        for ip in ip_list:
            ip = ip.split(":")
            ip_info = IpInfo(ip[0], ip[1], "", "", "")
            ip_infos.append(ip_info)
        return ip_infos
