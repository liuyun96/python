# -*- coding: utf8 -*-
# Filename: accesslog_process.pyimport MySQLdb
import sys
import codecs
import MySQLdb
import time
from datetime import *
reload(sys)
sys.setdefaultencoding('utf8')

class Report:
    #conn= MySQLdb.connect(host='10.241.6.33', user='root',passwd='43gz@2012,',charset = "utf8",db="dongji", use_unicode = True)
    conn = MySQLdb.connect(host='localhost', user='root', passwd='baijunli', charset="utf8", db="dongji", use_unicode=True)
    cursor = conn.cursor()

    def __init__(self,day):
        #self.path = '/home/43gz/top/'
        self.path = 'e:/'
        self.name_code = {'疯狂小鸟':'ts-18490', '疯狂标签':'ts-14632', '疯狂海报':'ts-14633', '疯狂橱窗':'ts-14085', '疯狂排名':'ts-29562'}
        self.name_key = {'疯狂小鸟':'12439296', '疯狂标签':'12368602', '疯狂海报':'12368608', '疯狂橱窗':'12327559', '疯狂排名':'12412369'}
        if len(sys.argv) == 2:
            self.today = sys.argv[1]
        else:
            self.today = (date.today() + timedelta(days=0)).strftime("%Y%m%d")
            self.weekAgo = (date.today() + timedelta(days= -day)).strftime("%Y%m%d")
    
    def userOrder(self,file):
        para_sql = {'免费版订购用户数':' and total_pay_fee=0', '付费版订购用户数':' and total_pay_fee!=0', '新订用户数':'', '续订用户':' and biz_type=2', '付费版到期用户数':'order_cycle_end >% s AND order_cycle_end <% s AND ARTICLE_CODE = % s and total_pay_fee!=0'}
        baseSql = ' SELECT COUNT(DISTINCT NICK) FROM ARTICLE_BIZ_ORDER WHERE '
        for name, code in self.name_code.items():
            file.write('--------' + name + '-------- \n')
            for key, sql in para_sql.items():
                if key == '付费版到期用户数' :
                    self.cursor.execute(baseSql + sql, (self.weekAgo, self.today, code));
                else:
                    self.cursor.execute(baseSql + ' CREATE_DATE >% s AND CREATE_DATE <% s AND ARTICLE_CODE = % s ' + sql, (self.weekAgo, self.today, code));
                rows = self.cursor.fetchall();
                if rows:
                     for row in rows:
                        file.write(key + ':' + str(row[0]) + '\n')
    
    def main(self):
        dt = datetime.now()
        week = dt.strftime('%U')
        txt = codecs.open(self.path+'week.txt', "wb", "utf-8");
        file = codecs.open(self.path+'report/'+str(date.today().year)+'_'+str(week)+'.txt', "wb", "utf-8");
        self.userOrder(txt)
        self.userOrder(file)
        txt.close()
        file.close()
        self.cursor.close()
        self.conn.close()

report = Report(6)
report.main()
