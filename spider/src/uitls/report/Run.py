# -*- coding: UTF-8 -*-
from crm_fkhb import CrmFkhb
from crm_fkbq import CrmFkbq
from crm_fkxn import CrmFkxn
from dict import apps
from seller_daily_log import SellerDailyLog
from DBConnection import ConnFactorty
from DBConnectionReport import ConnFactortyReport
from updateOrderTime import ARTICLE_BIZ_ORDER
from update_login_times import LoginTimes
import MySQLdb
import time
import datetime
import sys
from utils import MyUtil

class Run:
   def main(self):
       
       conn = ConnFactorty.getConn()
       cursor = conn.cursor()
       
       connReport = ConnFactortyReport.getConn()
       cursorReport = connReport.cursor()
       
       sysTime = datetime.datetime.now()
       print sysTime
       #同步日志信息
       log = SellerDailyLog(cursorReport)
       log.sycnData()
       myUtil = MyUtil() 
       
       for app in apps:
            #应用key
            key = app.key
            table = app.tableName
            code = app.code
            name = app.name
            #更新登入时间对象
            loginTimes = LoginTimes(table, key, cursor, cursorReport)
            #获取首次最大的免费订购时间，首次最大的付费订购时间
            cursor.execute(" select max(first_free_order_time) from " + table)
            maxFreeTime = cursor.fetchone()[0]
            cursor.execute(" select max(first_pay_order_time) from " + table)
            maxPayTime = cursor.fetchone()[0]
            
            max = maxFreeTime
            if maxPayTime > maxFreeTime:
                max = maxPayTime
            #当设置为None是全量同步
            #max = None
            #更新订购时间记录
            if True:
                #更新免费订购用户
                order1 = ARTICLE_BIZ_ORDER(app, cursor)
                order1.update(maxFreeTime)
                #更新付费订购用户
                order = ARTICLE_BIZ_ORDER(app, cursor)
                order.update(maxPayTime, '!')
                print table + ' 更新订购时间 已经完成暂 停 5秒 后更新每个应用独有指标'
                print myUtil.timediff(sysTime, datetime.datetime.now())   
                time.sleep(5)
            #更新 每个应用独有的指标
            if True:
                sql = ""
                if max != None:
                    print ' 最大订购时间 : ' + str(max);
                    max = datetime.datetime.strptime(max, '%Y-%m-%d %H:%M:%S').date().strftime('%Y%m%d')
                    #max.strftime("%Y%m%d")
                    sql = " and log_date >= '" + max + "'"
                #增量查询最近登入的用户
                cursorReport.execute(" select nick from SELLER_DAILY_LOG where app_key=%s " + sql + " group by nick", (key))
                nicks = cursorReport.fetchall()
                print ' 最近登入的用户数   : ' + str(len(nicks)) 
                for row in nicks:
                    try:
                        nick = row[0]
                        cursor.execute(" select user_id from TOP_SELLER where nick = %s ", (nick))
                        rows = cursor.fetchone()
                        if rows != None:
                           #更新登入次数
                           loginTimes.updateTimes(nick)
                           #更新每个应用指标
                           user_id = rows[0]
                           if name == '疯狂海报':
                               crmFkhb = CrmFkhb(nick, cursor, str(user_id))
                               crmFkhb.updatePlaNum()
                           elif name == '疯狂标签':
                               crm_fkbq = CrmFkbq(nick, cursor, str(user_id))
                               crm_fkbq.updateTagNum()
                           elif name == '疯狂小鸟':    
                               crm_fkxn = CrmFkxn(nick, cursor, str(user_id))
                               crm_fkxn.updateIsActivity()
                    except:
                        print sys.exc_info()[0], sys.exc_info()[1]
                    
                print table + ' 更新每个应用独有指标已经完成 ,暂 停 5秒 后 更新登入次数'
                print myUtil.timediff(sysTime, datetime.datetime.now())   
                time.sleep(5)
            #更新登入次数
            if True:
                loginTimes.update()
                print table + ' 更新登入次数完成 '  
                print myUtil.timediff(sysTime, datetime.datetime.now())
                     
       cursor.close()
       conn.close()
       
       cursorReport.close()
       connReport.close()
       
run = Run()
run.main()

