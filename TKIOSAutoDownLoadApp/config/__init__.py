class TK_Config:

    def __init__(self, downApplink, app_bundle_id, app_report_link, app_report_flag):
        self.downApplink = downApplink
        self.app_bundle_id = app_bundle_id
        self.app_report_link = app_report_link
        self.app_report_flag = app_report_flag

    def get_downApplink(self):
        return self.downApplink

    def get_app_bundle_id(self):
        return self.app_bundle_id

    def get_app_report_link(self):
        return self.app_report_link

    def get_app_report_flag(self):
        return self.app_report_flag


config = None


def init(downApplink, app_bundle_id, app_report_link, app_report_flag):
    global config
    if not config:
        config = TK_Config(downApplink, app_bundle_id, app_report_link, app_report_flag)


def getConfig():
    global config
    if not config:
        raise Exception("you must perform init method befor getConfig method")
    return config
