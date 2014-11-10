# -*- coding: utf8 -*-
# Filename: Chat.py
import MySQLdb
import sys
import codecs
import time
import datetime
from datetime import date, timedelta
from DBConnection import ConnFactorty
reload(sys) 
sys.setdefaultencoding('utf-8')

class Total(object):
    def __init__(self, conn, status):
        self.status = status;
        self.cursor = conn.cursor();
    #计算转化量
    def zhuanHL(self, user, startDate):
        endDate = (startDate + timedelta(days=1)).strftime("%Y-%m-%d")
        endD = (startDate + timedelta(days= -2)).strftime("%Y-%m-%d")
        sql = " select nick,total_pay_fee,create_date from ARTICLE_BIZ_ORDER where create_date>%s and create_date<%s and total_pay_fee!=0 ";
        self.cursor.execute(sql, (startDate, endDate))
        #print ' startDate ' + str(startDate) + ' endDate: ' + str(endDate) + ' endD: ' + str(endD);
        results = self.cursor.fetchall()
        val = 0;
        sellers = '';
        for r in results:
            seller = r[0];
            value = r[1];
            create_date = r[2];
            #查看前三天的聊天记录
            sql = " select min(start_chat_date) from CHAT_TOTAL where user=%s and seller=%s and date <= %s and date > %s  and status = %s "
            self.cursor.execute(sql, (user.name, seller, startDate, endD, self.status))
            start_chat_date = self.cursor.fetchone();
            if start_chat_date[0] != None and value != None:
                if start_chat_date[0] <= create_date:
                    if int(value) < 6000:
                        val += 1;
                    else:
                        val += 2;
                    sellers += seller + ','; 
        if sellers != '':
            #print user.nick + ' zhuanHL: ' + str(val);
            sellers = '[下单卖家:' + sellers + ' 金币:' + str(val) + '],';
        return {'value': val, "sellers":sellers, 'date':startDate};
    
    #如果已经添加过金币，就修改状态
    def updateStatus(self, user, yesterday):
        sql = " update CHAT_TOTAL set status = 1 where user =%s and date = %s and status = 0 "
        self.cursor.execute(sql, (user.name, yesterday));
    #直通车客服
    def zhiTC(self, user, yesterday):
        zhd = self.zhuanHL(user, yesterday);
        remark = zhd['sellers'];
        zhv = zhd['value'];
        val = 0;
        sql = " select count(*) from CHAT_TOTAL where user =%s and date = %s and num>%s and status = %s "
        self.cursor.execute(sql, (user.name, yesterday, 3, self.status))
        value = self.cursor.fetchone();
        p = 5;
        if value[0] != None and value[0] != 0:
           remark += '[聊天记录:' + str(value[0]) + ']';
           val = int(value[0]) - 20;
           if val > 0:
               val = ((val + p - 1) / p) + zhv; 
           else:
               val = zhv;
        else:
           val = zhv;
        return {'value':val, 'remark':remark, 'date':yesterday};
    #普通客服
    def keFu(self, user, yesterday):
        zhd = self.zhuanHL(user, yesterday);
        remark = zhd['sellers'];
        zhv = zhd['value'];
        val = 0;
        sql = " select count(*) from CHAT_TOTAL where user =%s and date = %s and num>%s and status = %s "
        self.cursor.execute(sql, (user.name, yesterday, 3, self.status))
        value = self.cursor.fetchone();
        p = 10;
        if value[0] != None and value[0] != 0:
           remark += '[聊天记录数:' + str(value[0]) + ']';
           val = int(value[0]) - 30;
           if val > 0:
               val = ((val + p - 1) / p) + zhv;
           else:
               val = zhv;
        else:
            val = zhv;
        return {'value':val, 'remark':remark, 'date':yesterday};
    #根据用户名称取出还未统计的用户记录
    def getDates(self, user):
         self.cursor.execute(''' select date from CHAT_TOTAL where user=%s and status=%s group by date
                            ''', (user, self.status))
         return self.cursor.fetchall();
