# -*- coding: UTF-8 -*-
from crm_report import Report
class Access:
    def __init__(self, cursor, cursorReport, app_key, log_date, id):
        self.cursorReport = cursorReport;
        self.cursor = cursor;
        self.app_key = app_key;
        self.log_date = log_date;
        self.id = id
    #登入用户数
    def login_num(self):
        self.cursorReport.execute(" select count(*) from SELLER_DAILY_LOG where app_key=%s and log_date = %s ",
                            (self.app_key, self.log_date))
        users = self.cursorReport.fetchone();
        report = Report(self.cursor, 'login_num', users, self.id)
        return report.update();
    
    
