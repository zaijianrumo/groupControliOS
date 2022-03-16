# -*- coding: utf-8 -*-

import yaml
from TKIOSAutoDownLoadApp.baseConfg.baseAppiumServer import *
from TKIOSAutoDownLoadApp.baseConfg.desired_capabilities import *

# 构建desired进程组
desired_process = []


def runnerPool(getDevices):

    for i in range(0, len(getDevices)):
        udid = getDevices[i]['udid']
        port = getDevices[i]["port"]
        wdaPort = getDevices[i]["wdaPort"]
        desired = multiprocessing.Process(target=MyDesiredCapabilities().get_desired_capabilities,
                                          args=(udid, str(port), str(wdaPort)))
        desired_process.append(desired)
        # 启动多设备执行测试
    for desired in desired_process:
        desired.start()
        # 等所有进程结束后关闭
    for desired in desired_process:
        desired.join()


def runnerCaseApp(devicess):
    suite = unittest.TestSuite()
    suite.addTest(mainAppTest_01())
    unittest.TextTestRunner(verbosity=2).run(suite)

def mainAppTest_01(self):
    pass


if __name__ == '__main__':
    # 获取配置设备
    dev_iOS = PATH("../yamlConfig/devices_info.yaml")
    with open(dev_iOS, encoding='utf-8') as stream:
        try:
            init_args = yaml.load(stream, Loader=yaml.Loader)
            print(init_args)
        except Exception as e:
            print(e)
    if len(init_args) > 0:
        infos = []
        for dev in init_args:
            app = {}
            app["udid"] = dev["udid"]
            app["port"] = dev["port"]
            app["wdaPort"] = dev["wdaport"]
            infos.append(app)
        appium_server = AppiumServer(infos)
        appium_server.start_server()
        runnerPool(infos)


