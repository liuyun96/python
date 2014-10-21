# -*- coding: UTF-8 -*-
from DBConnectionReport import ConnFactortyReport
from DBConnection import ConnFactorty
from seller_daily_log import SellerDailyLog
from update_login_times import LoginTimes
from dict import tables, codes, keys
import time
import datetime
import MySQLdb

class Run:
   def main(self):
       
       conn = ConnFactorty.getConn()
       cursor = conn.cursor()
       connReport = ConnFactortyReport.getConn()
       cursorReport = connReport.cursor()
       
       loginTimes = LoginTimes(tables['fkbq'], keys['fkbq'], cursor, cursorReport)
       loginTimes.update()
       
       
       cursor.close()
       conn.close()
       cursorReport.close()
       connReport.close()
       
run = Run()
run.main()


