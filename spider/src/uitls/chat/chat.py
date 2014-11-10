# -*- coding: utf8 -*-
# Filename: Chat.py
import sys
import codecs
import time
import datetime
from datetime import date, timedelta
reload(sys) 
sys.setdefaultencoding('utf-8') 

class Chat(object):
    
    def __init__(self, conn):
        self.cursor = conn.cursor();
    def checkDate(self, user, date):
        self.cursor.execute(''' select count(*) from CHAT_REPORT where user=%s and date=%s
                            ''', (user, date))
        value = self.cursor.fetchone();
        if value[0] != 0:
            return True;
        return False;
    
    def getDate(self, user):
        self.cursor.execute(''' select max(date) from CHAT_REPORT where user=%s 
                            ''', (user))
        value = self.cursor.fetchone();
        if value[0] != None:
            max = datetime.datetime.strptime(str(value[0]), '%Y-%m-%d %H:%M:%S').date().strftime('%Y-%m-%d')
            max = datetime.datetime.strptime(max, '%Y-%m-%d');
            return max;
        return None;
    
    def checkTotal(self, user, d):
        self.cursor.execute(''' select count(*) from CHAT_TOTAL where user=%s and date=%s
                            ''', (user, d))
        value = self.cursor.fetchone();
        if value[0] != 0:
            return False;
        return True;
    
    def total(self, user, d):
        #判断是否已经保存过了
        check = self.checkTotal(user, d);
        d = datetime.datetime.strptime(d, '%Y%m%d');
        d1 = (d + timedelta(days=1)).strftime("%Y-%m-%d");
        d = d.strftime('%Y-%m-%d');
        if check:
            self.cursor.execute(''' select seller,count(*) from CHAT_REPORT where user=%s and date>=%s and date<%s group by seller
                                ''', (user, d, d1))
            sellers = self.cursor.fetchall()
            for s in sellers:
                seller = s[0]
                num = s[1]
                self.cursor.execute(''' select min(date),max(date) from CHAT_REPORT where user=%s and date>=%s and date<%s and seller=%s
                                ''', (user, d, d1, seller));
                value = self.cursor.fetchone();
                if value != None:
                    start = value[0];
                    end = value[1];
                    #print user + str(end) + str(d)
                    self.saveTotal(user, seller, num, start, end, d);
            
    def saveTotal(self, user, seller, num, start, end, d):
        self.cursor.execute('''
                            insert into CHAT_TOTAL(user,seller,num,start_chat_date,end_chat_date,date,status)
                            VALUES (%s,%s,%s,%s,%s,%s,0)
                            ''', (user, seller, num, start, end, d))
    #删除数据
    def deleteData(self):
        week = (date.today() + timedelta(days= -31)).strftime("%Y-%m-%d")
        self.cursor.execute(' delete from CHAT_REPORT where date < %s ', (week))
    def saveReport(self, path):
        f = codecs.open(path, encoding='GBK')
        user = ''; 
        check = False;
        while True:
            try:
                line = f.readline()
                if user == '' and line.find('思正科技:大副') != -1:
                   user = '大副';
                elif user == '' and line.find('思正科技:船长') != -1:
                    user = '船长'; 
                elif user == '' and line.find('思正科技:舵手') != -1:
                    user = '舵手';
                if len(line) == 0:
                    break;
                d = line.find('日')
                #有时间的
                if user != '' and d != -1:
                    t = line[0:20].replace('年', '-').replace('月', '-').replace('日', ' ');
                    start = line.find(':', 20);
                    content = line[start + 1:]
                    if line.find('思正科技') == -1:
                        if check == False:
                            check = self.checkDate(user, t);
                            if check:
                                break;
                            check = True;
                        seller = line[20:start]
                        self.cursor.execute('''
                            insert into CHAT_REPORT(user,seller,content,date)
                            VALUES (%s,%s,%s,%s)
                            ''', (user, seller, content, t))
            except:
                    print '读取文件发生异常,文件路径:' + path
        #关闭文件流 和数据库
        f.close();        
        return user;

