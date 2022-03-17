# from browser import BrowserBuilder, utils
# from proxy_ip.impl.proxy_ip_interface import ProxyIpAbstract
# from proxy_ip.ip_info import IpInfo
#
#
# class FreeIp(ProxyIpAbstract):
#     """
#     到https://www.kuaidaili.com/free/inha/{}/网站爬取ip
#     """
#     __MAX_PAGE = 100
#
#     def __init__(self):
#         self.__current_page = 1
#
#     def get_proxy_ip(self, size):
#         browser = BrowserBuilder(headless=False).get_browser()
#         result_list = []
#         for i in range(self.__current_page, FreeIp.__MAX_PAGE):
#             browser.get("https://www.kuaidaili.com/free/inha/{}/".format(i))
#             table = browser.find_element_by_xpath("//div[@id='list']/table")
#             # 解析表格
#             table_list = utils.resolver_table(table)
#             ip_infos = self.__resolver_table_list(table_list)
#             for ip_info in ip_infos:
#                 result_list.append(ip_info)
#                 if len(result_list) >= size:
#                     self.__reset_current_page(i + 1)
#                     browser.quit()
#                     return result_list
#
#     def __reset_current_page(self, page):
#         if page < FreeIp.__MAX_PAGE:
#             self.__current_page = page
#         else:
#             self.__current_page = 1
#
#     def __resolver_table_list(self, table_list: list):
#         if len(table_list) == 0:
#             return table_list
#         result_list = []
#         for item in table_list:
#             ip_info = IpInfo(item.get('IP'), item.get('PORT'), item.get('响应速度'), item.get('最后验证时间'),
#                              item.get('位置'), item.get('类型'), item.get('匿名度'))
#             result_list.append(ip_info)
#         return result_list
