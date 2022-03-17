"""
    获取爬取代理ip地址获取代理ip、
    向外提供代理ip
    一次爬取若干条ip,若当前存储的ip少于阀值条就再次进行爬取
"""
import logging
import threading
from queue import Queue

from TKIOSAutoDownLoadApp.proxy_ip.impl import ProxyIpAbstract, TianQiIp
from TKIOSAutoDownLoadApp.proxy_ip.ip_info import IpInfo


class ProxyIp:

    def __init__(self, maxsize=2, threshold=2, proxy_ip_impl: ProxyIpAbstract = TianQiIp()):
        """
        创建一个代理ip
        :param maxsize: 缓存的最大值
        :param threshold: 阀值，当剩余代理ip小于这个阀值的时候会再次去代理ip的实现中再次获取ip
        :param proxy_ip_impl: 代理ip的实现,一定要继承ProxyIpAbstract类
        """
        self.__proxy_ip = Queue(maxsize=maxsize)
        self.__threshold = threshold
        self.__proxy_ip_impl: ProxyIpAbstract = proxy_ip_impl
        self.__lock = threading.Lock()
        self.__log = logging.getLogger("sys.proxy_ip")
        # 首次初始化代理ip队列
        self.__refresh_proxy_ip()

    def __refresh_proxy_ip(self):
        empty_size = self.__proxy_ip.maxsize - self.__proxy_ip.qsize()
        ip_infos = self.__proxy_ip_impl.get_proxy_ip(empty_size)
        for ip_info in ip_infos:
            if self.__proxy_ip.full():
                break
            # 不会阻塞，但是满了会报错!别慌，前面都进行加锁了
            self.__proxy_ip.put_nowait(ip_info)

    def get_proxy_ip_info(self) -> IpInfo:
        """
        返回一个代理ip
        双重自检锁用于防止大并发的场景
        :return: 代理ip
        """
        if self.__proxy_ip.qsize() < self.__threshold:
            self.__lock.acquire()
            try:
                if self.__proxy_ip.qsize() < self.__threshold:
                    self.__refresh_proxy_ip()
            finally:
                self.__lock.release()

        if self.__proxy_ip.empty() == False:
            return self.__proxy_ip.get()
        else:
            # 这个基本不会走到的，因为前面都不小于10个了
            return "127.0.0.1"

    def get_proxy_server(self) -> str:
        ip_info: IpInfo = self.get_proxy_ip_info()
        proxy_server = ip_info.get_proxy_server()
        # self.__log.debug("get proxy server: {}".format(proxy_server))
        return proxy_server


if __name__ == '__main__':
    proxy_ip = ProxyIp(maxsize=2, threshold=2, proxy_ip_impl=TianQiIp())
    for i in range(5):
        print(proxy_ip.get_proxy_server())
