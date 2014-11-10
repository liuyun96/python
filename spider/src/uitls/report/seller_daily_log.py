# -*- coding: UTF-8 -*-
from datetime import date, timedelta
class SellerDailyLog:
    def __init__(self, connReport):
        self.cursor = connReport
    def sycnData(self):
        half_year = (date.today() + timedelta(days= -180)).strftime("%Y%m%d")
        self.cursor.execute(" select max(log_date) from SELLER_DAILY_LOG ")
        maxLogDate = self.cursor.fetchone()
        sql = " select nick_name,app_key,DATE_FORMAT(LOG_TIME,'%%Y%%m%%d') from ACCESS_LOG where log_time > %s group by nick_name,app_key,DATE_FORMAT(LOG_TIME,'%%Y%%m%%d') "
        if maxLogDate[0] != None:
            self.cursor.execute(sql, (maxLogDate[0]))
        else:
            self.cursor.execute(sql, (half_year))
        logs = self.cursor.fetchall()
        for log in logs:
            nick = log[0]
            appKey = log[1]
            logDate = log[2]
            #把数据插入日志表
            self.cursor.execute('insert into SELLER_DAILY_LOG(nick,app_key,log_date) values(%s,%s,%s)', (nick, appKey, logDate))
        print 'sycnData SELLER_DAILY_LOG finish '
        #删除半年前的数据
        #self.cursor.execute(' delete from SELLER_DAILY_LOG where log_date < %s ', (half_year))
        print 'delete SELLER_DAILY_LOG success before half a year '
        
            
        






