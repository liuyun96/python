# -*- coding: UTF-8 -*-
import MySQLdb
from datetime import datetime, time
import datetime  
import time

class MyUtil:    
    def timediff(self, timestart, timestop):  
        t = (timestop - timestart)  
        time_day = t.days  
        s_time = t.seconds  
        ms_time = t.microseconds / 1000000  
        usedtime = int(s_time + ms_time)  
        time_hour = usedtime / 60 / 60  
        time_minute = (usedtime - time_hour * 3600) / 60  
        time_second = usedtime - time_hour * 3600 - time_minute * 60  
        time_micsecond = (t.microseconds - t.microseconds / 1000000) / 1000  
        #retstr = "%d天%d小时%d分%d秒%d毫秒" % (time_day, time_hour, time_minute, time_second, time_micsecond)
        retstr = " execute %d小时%d分%d秒%d毫秒" % (time_hour, time_minute, time_second, time_micsecond)
        return retstr

#startTime = datetime.datetime.now()
#time.sleep(5)
#endTime = datetime.datetime.now()
#myUtil = MyUtil()
#print myUtil.timediff(startTime, endTime)

    
    
    
