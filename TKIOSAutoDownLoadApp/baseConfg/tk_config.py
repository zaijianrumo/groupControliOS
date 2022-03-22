class TK_Config:

    def __init__(self, downApplink, app_bundle_id, app_report_link):
        self.downApplink = downApplink
        self.app_bundle_id = app_bundle_id
        self.app_report_link = app_report_link

    def get_downApplink(self):
        return self.downApplink

    def get_app_bundle_id(self):
        return self.app_bundle_id

    def get_app_report_link(self):
        return self.app_report_link
