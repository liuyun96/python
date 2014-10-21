# -*- coding: UTF-8 -*-
from crm_fkhb import CrmFkhb
from crm_fkbq import CrmFkbq
from crm_fkxn import CrmFkxn
from dict import codes,code_table,code_key
from seller_daily_log import SellerDailyLog
from DBConnection import ConnFactorty
from updateOrderTime import ARTICLE_BIZ_ORDER
from update_login_times import LoginTimes
import time
import datetime
import sys
from utils import MyUtil

class Report:
   def main(self):
       conn = ConnFactorty.getConn()
       cursor = conn.cursor()
       for code, table in code_table.items():
           cursor.execute(" select j,count(*) c from (select (to_days(first_pay_order_time)-to_days(first_free_order_time)) " +
           " as j from "+table+" where first_pay_order_time is not null and first_free_order_time is not null) t where j>=0 and j<=30  group by j order by j ")
           rows = cursor.fetchall()
           print table+' 既订购 了免费版又订购了高级版的用户'
           print '相隔天数    人数' 
           for row in rows:
               timediff = row[0]
               count = row[1]
               print '   '+str(timediff) +'      '+ str(count)
           
           cursor.execute(" select count(*) from " +table+ " where first_pay_order_time is not null and first_free_order_time is null ")
           rows = cursor.fetchall()
           print table+' 直接订购了高级版的用户  '
           for row in rows:
               count = row[0]
               print count
               
           cursor.execute(" select count(*) from "+table+" where first_pay_order_time is null and first_free_order_time is not null ")
           rows = cursor.fetchall()
           print table+' 只订购免费版的用户  '
           for row in rows:
               count = row[0]
               print count
       
       cursor.close()
       conn.close()
report = Report()
report.main()

