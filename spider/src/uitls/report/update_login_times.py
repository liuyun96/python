# -*- coding: UTF-8 -*-
from datetime import date, timedelta

class LoginTimes:
    def __init__(self, tableName, appKey, cursor, cursorReport):
        self.cursor = cursor
        self.cursorReport = cursorReport
        self.tableName = tableName
        self.appKey = appKey
    def updateTimes(self, nick):
        week = (date.today() + timedelta(days= -7)).strftime("%Y%m%d")
        month = (date.today() + timedelta(days= -30)).strftime("%Y%m%d")
        half_year = (date.today() + timedelta(days= -180)).strftime("%Y%m%d")
        
        sql = " select count(*) from SELLER_DAILY_LOG where app_key=" + self.appKey + " and nick = '" + nick + "' and log_date >= %s "
        self.cursorReport.execute(sql, (half_year))
        half_year_login_times = self.cursorReport.fetchone()
        halfTimes = 0
        monthTimes = 0
        weekTimes = 0 
        
        if half_year_login_times != None:
            halfTimes = half_year_login_times[0]
        if  halfTimes != 0:
            self.cursorReport.execute(sql, (month))
            month_login_times = self.cursorReport.fetchone()
            if month_login_times != None:
                monthTimes = month_login_times[0]
        if monthTimes != 0:   
            self.cursorReport.execute(sql, (week))
            week_login_times = self.cursorReport.fetchone()
            if week_login_times != None:
                weekTimes = week_login_times[0]
        if halfTimes != 0 :
            self.cursor.execute('update ' + self.tableName + '  set week_login_times=%s,month_login_times=%s,half_year_login_times=%s,update_time=%s where seller_nick=%s ',
             (weekTimes, monthTimes, halfTimes, date.today(), nick))

    #Run调用此方法更新最近未登入的用户登入次数
    def update(self):
       cursor = self.cursor
       table = self.tableName
       sql = ' where half_year_login_times !=0 and update_time != "' + str(date.today()) + '"';
       cursor.execute(" select count(*) from " + table + sql)
       total = cursor.fetchone()
       print ' 需要更新登入次数总条数    : ' + str(total[0]);
       pageSize = 5000
       pageNo = (int(total[0]) + pageSize - 1) / pageSize
       start = 0
       for i in range(1, pageNo + 1):
            print str(start) + ':' + self.appKey
            cursor.execute(" select seller_nick from " + table + sql + " limit %s,%s", (start, pageSize))
            orders = cursor.fetchall()
            for o in orders:
                nick = o[0]
                self.updateTimes(nick)
            start = pageSize * i
          

