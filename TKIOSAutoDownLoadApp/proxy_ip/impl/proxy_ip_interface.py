import abc


class ProxyIpAbstract(metaclass=abc.ABCMeta):
    """
    用来约束代理ip服务
    """

    @abc.abstractmethod
    def get_proxy_ip(self, size) -> list:
        """
        获取一个代理ip信息的列表 {@see #IpInfo},
        注意！！！返回的ip列表元素一定要被IpInfo封装
        :param size: 返回的条数
        :return: 被IpInfo封装的ip列表对象
        """
        pass

