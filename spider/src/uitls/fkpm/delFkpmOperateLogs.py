# -*- coding: utf8 -*-
# Filename: delFkpmOperateLogs.py
import MySQLdb
import sys
from datetime import date, timedelta
import time

reload(sys)
sys.setdefaultencoding('utf8')

print '启动fkpm日志的清理程序，表名:FKPM_OPERATE_LOGS'
print time.time()

conn = MySQLdb.connect(host='s13', user='dongji', passwd='dongji0okm', charset="utf8", db="dongji", use_unicode=True)
#conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', charset="utf8", db="dongji", use_unicode=True)
cursor = conn.cursor()

half_a_month_ago = (date.today() + timedelta(days= -15)).strftime("%Y-%m-%d 00:00:00")
print '开始清理 ' + half_a_month_ago + ' 以前的数据'

cursor.execute('''DELETE FROM FKPM_OPERATE_LOGS WHERE OPER_TIME<%s''', half_a_month_ago)
conn.commit();
conn.close();

print time.time()
print '清理结束'


