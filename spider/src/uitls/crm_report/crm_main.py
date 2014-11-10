# -*- coding: UTF-8 -*-
from DBConnection import ConnFactorty
from DBConnectionReport import ConnFactortyReport
from datetime import date, timedelta
from dict import allApp
import time
import datetime
import sys
from crm_report import Report
from biz_order import BizOrder
from pv_uv import LineZing
from crm_access import Access
from crm_app_detail import AppDetail

class Run:
    def main(self):
       #try:
           #day = datetime.datetime.strptime('2012-04-13', "%Y-%m-%d")  
           day = date.today()
           today = (day + timedelta(days=0)).strftime("%Y%m%d")
           yesterday = (day + timedelta(days= -1)).strftime("%Y%m%d")
           
           conn = ConnFactorty.getConn()
           cursor = conn.cursor()
           
           connReport = ConnFactortyReport.getConn()
           cursorReport = connReport.cursor()
           
           if True:
               ids = {}
               for app in allApp:
                   cursor.execute(" select id from CRM_REPORT where app_name=%s and create_date=%s ", (app.name, yesterday));
                   id = cursor.fetchone();
                   if id != None:
                       id = id[0];
                   order = BizOrder(cursor, yesterday, today, app, id);
                   #新增用户
                   order.new_user();
                   cursor.execute(" select id from CRM_REPORT where app_name=%s and create_date=%s ", (app.name, yesterday));
                   id = cursor.fetchone();
                   if id != None:
                       id = id[0]
                       
                       order = BizOrder(cursor, yesterday, today, app, id);
                       #新付费用户
                       order.new_pay_user();
                       order.new_order();
                       order.pay_order();
                       order.pay(); 
                       order.old_user_order();
                       order.old_user_pay();
                   
                   #量子应用
                   ids[app.name] = id;
               
               #更新量子数据    
               lineZing = LineZing(cursor);
               lineZing.update_pv_uv(ids)
           
           
           if True:
               for app in allApp:
                   cursor.execute(" select id from CRM_REPORT where app_name=%s and create_date=%s ", (app.name, yesterday));
                   id = cursor.fetchone();
                   if id != None:
                       id = id[0]
                       order = BizOrder(cursor, yesterday, today, app, id);
                       order.order_rate();
                       order.pay_rate();
                       order.input_output_ratio();
                       order.unit_price();
                       order.renewr_rate();
                       
                       
                       access = Access(cursor, cursorReport, app.key, yesterday, id);
                       access.login_num()
                       
                       appDatail = AppDetail(cursor, app.code, id);
                       appDatail.parser();
           
           cursor.close()
           conn.close()
           connReport.close()
           connReport.close()
       #except:
           #print sys.exc_info()[0], sys.exc_info()[1]
        
run = Run()
run.main()
