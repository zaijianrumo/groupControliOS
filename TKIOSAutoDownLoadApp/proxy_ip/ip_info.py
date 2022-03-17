"""
承载代理ip的信息
"""


class IpInfo:

    def __init__(self, ip: str, port: str, response_speed: str, time: str, location: str, type='http',
                 anonymous_degrees='高匿名'):
        """
        :param ip: ip
        :param port: 端口
        :param response_speed: 响应速度
        :param time: 最后验证时间
        :param location: 地理位置
        :param type: 网络类型
        :param anonymous_degrees: 匿名度
        """
        self.__ip = ip
        self.__port = port
        self.__response_speed = response_speed
        self.__time = time
        self.__location = location
        self.__type = type
        self.__anonymous_degrees = anonymous_degrees

    def get_proxy_server(self):
        return self.__type.lower() + "://" + self.__ip + ":" + self.__port

    def __str__(self):
        return "IpInfo(ip=" + self.__ip + ", port=" + self.__port + ", response_speed=" + self.__response_speed \
               + ", time=" + self.__time + ", location=" + self.__location + ", type=" + self.__type \
               + ", anonymous_degrees=" + self.__anonymous_degrees + ")"

    def get_ip(self):
        return self.__ip

    def get_port(self):
        return self.__port
