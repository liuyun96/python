# -*- coding: UTF-8 -*-
import MySQLdb
from datetime import datetime, time
import datetime  
from datetime import date, timedelta
import time

def timediff(timestart, timestop):  
       t = (timestop - timestart)  
       time_day = t.days  
       s_time = t.seconds  
       ms_time = t.microseconds / 1000000  
       usedtime = int(s_time + ms_time)  
       time_hour = usedtime / 60 / 60  
       time_minute = (usedtime - time_hour * 3600) / 60  
       time_second = usedtime - time_hour * 3600 - time_minute * 60  
       time_micsecond = (t.microseconds - t.microseconds / 1000000) / 1000  
  
       retstr = "%d天%d小时%d分%d秒%d毫秒" % (time_day, time_hour, time_minute, time_second, time_micsecond)  
       return retstr
   
#print timediff(datetime.datetime, time.strftime('2012.12.12'))  

#startTime = datetime.datetime.now()
#time.sleep(5)
#endTime = datetime.datetime.now()

#print timediff(startTime,endTime)
date = datetime.datetime.strptime('20121212','%Y%m%d').date()
print date.strftime('%Y%m%d')
    
    
    
