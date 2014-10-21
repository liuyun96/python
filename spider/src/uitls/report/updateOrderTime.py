# -*- coding: UTF-8 -*-
import MySQLdb
from datetime import date, timedelta
import time
from DBConnection import ConnFactorty
import sys

class ARTICLE_BIZ_ORDER:
    
    def __init__(self, app, cursor):
        self.cursor = cursor
        self.tableName = app.tableName
        self.article_code = app.code
            
    #保存修改  免费订购时间           
    def saveOrUpdateFreeTime(self, nick, create_date, order_cycle_end, isSave):
        try:
            if(isSave == 'update'):
                self.cursor.execute(" update " + self.tableName + " set first_free_order_time=%s,free_end_time=%s where seller_nick = %s " ,
                                    (create_date, order_cycle_end, nick))
            elif isSave == 'save':
                self.cursor.execute(" insert into " + self.tableName + " (seller_nick,first_free_order_time,free_end_time) values (%s,%s,%s)" ,
                                    (nick, create_date, order_cycle_end))
        except:
           print isSave + '用户:' + nick + '' + create_date + '' + order_cycle_end
           print sys.exc_info()[0], sys.exc_info()[1]   
   #Run调用此方法更新订购时间     
    def update(self, maxTime, isFee=''):
       try:
           cursor = self.cursor
           table = self.tableName
           code = self.article_code
           sql = " "
           if maxTime != None:
               sql = " and create_date >= '" + maxTime + "'"
           cursor.execute("select count(*) from (select count(*) from ARTICLE_BIZ_ORDER where article_code = %s and total_pay_fee" + isFee + "='0' " + sql + " group by nick ) t", (code))
           total = cursor.fetchone()
           print isFee + ' 免费需要更新订购时间的总条数   : ' + str(total[0])
           print isFee + ' 免费最大时间订购时间   : ' + str(maxTime)
           pageSize = 5000
           pageNo = (int(total[0]) + pageSize - 1) / pageSize
           start = 0
           for i in range(1, pageNo + 1):
                cursor.execute(" select nick,max(create_date),order_cycle_end from ARTICLE_BIZ_ORDER where article_code = %s " + sql + " and total_pay_fee" + isFee + "='0' group by nick order by max(create_date) limit %s,%s ", (code, start, pageSize))
                orders = cursor.fetchall()
                for o in orders:
                    nick = o[0]
                    create_date = o[1]
                    order_cycle_end = o[2]
                    
                    #根据昵称 表名查询 记录是否存在
                    cursor.execute(' select update_time from ' + self.tableName + ' where seller_nick = %s ', (nick))
                    update_time = self.cursor.fetchone()
                    
                    isSave = 'update'
                    if update_time == None:
                        isSave = 'save'
                    elif update_time != date.today():
                        isSave = 'update'
            
                    if isFee == '':
                        #print self.article_code + ' ' + isSave + 'FreeTime ' + nick + ' ' + str(create_date)
                        self.saveOrUpdateFreeTime(nick, create_date, order_cycle_end, isSave)
                    else:
                        #print self.article_code + ' ' + isSave + 'PayTime ' + nick + ' ' + str(create_date)
                        self.saveOrUpdatePayTime(nick, create_date, order_cycle_end, isSave)     
                start = pageSize * i
                
       except:
           print isSave + '用户:' + nick
           print sys.exc_info()[0], sys.exc_info()[1]   
           

    #修改付费订购时间
    def saveOrUpdatePayTime(self, nick, create_date, order_cycle_end, isSave):
        if isSave == 'save':
            self.cursor.execute(' insert into ' + self.tableName + ' (seller_nick,first_pay_order_time,pay_end_time) values (%s,%s,%s) ',
                 (nick, create_date, order_cycle_end))
        elif(isSave == 'update'):
            self.cursor.execute(' update ' + self.tableName + ' set first_pay_order_time=%s,pay_end_time=%s where seller_nick = %s ',
                                (create_date, order_cycle_end, nick))
                       

