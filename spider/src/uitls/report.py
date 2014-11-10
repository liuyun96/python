# -*- coding: utf8 -*-
# Filename: accesslog_process.py
from datetime import date, timedelta
import re
import MySQLdb
import sys
import traceback
import codecs
import time
from dict import allApp
from linezing import LineZing

reload(sys)
sys.setdefaultencoding('utf8')

if len(sys.argv) == 2:
    today = sys.argv[1]
else:
    today = (date.today() + timedelta(days=0)).strftime("%Y%m%d")
    yesterday = (date.today() + timedelta(days= -1)).strftime("%Y%m%d")
    firstDayOfMonth = date(date.today().year, date.today().month, 1).strftime("%Y%m%d")
    firstDayOfYear = date(date.today().year, 1, 1).strftime("%Y%m%d")
filename = '/home/43gz/top/report/' + today + '.txt';
f = codecs.open(filename, "wb", "utf-8");
f2 = codecs.open('/home/43gz/top/report.txt', "wb", "utf-8");

def write(line):
    f.write(line)
    f2.write(line)
    
line = u'最后更新时间:' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n';
write(line)

conn = MySQLdb.connect(host='10.241.6.33', user='root', passwd='43gz@2012,', charset="utf8", db="dongji", use_unicode=True)
cursor = conn.cursor()
conn2 = MySQLdb.connect(host='10.241.118.37', user='report', passwd='report12344321', charset="utf8", db="report", use_unicode=True)
cursor2 = conn2.cursor()

cursor.execute('''
    SELECT SUM(REFUND_FEE+TOTAL_PAY_FEE)/100.0 FROM ARTICLE_BIZ_ORDER WHERE TOTAL_PAY_FEE>0 AND CREATE_DATE>%s
''', today)
rows = cursor.fetchall()
if rows:
    for row in rows:
        write(u'今日共计:' + str(row[0]) + u'详细如下：\n');

cursor.execute('''
    SELECT ARTICLE_NAME,(REFUND_FEE+TOTAL_PAY_FEE)/100.0,ORDER_CYCLE,NICK,CREATE_DATE FROM ARTICLE_BIZ_ORDER WHERE TOTAL_PAY_FEE>0 AND CREATE_DATE>%s
''', today)
rows = cursor.fetchall();
if rows:
    for row in rows:
        line = row[0] + '(' + row[2] + ')' + ',' + str(row[1]) + ',' + row[3] + ',' + str(row[4]) + '\n';
        write(line);
        
cursor.execute('''
    SELECT ARTICLE_NAME,COUNT(DISTINCT NICK) FROM ARTICLE_BIZ_ORDER WHERE CREATE_DATE>%s group by ARTICLE_NAME
''', today)

write(u'今日新增用户数:\n');

rows = cursor.fetchall();
if rows:
    for row in rows:
        write(row[0] + ',' + str(row[1]) + '\n');
        
cursor.execute('''
    SELECT DATE_FORMAT(CREATE_DATE,'%%Y-%%m-%%d') ,SUM(REFUND_FEE+TOTAL_PAY_FEE)/100.0  FROM ARTICLE_BIZ_ORDER 
WHERE  CREATE_DATE >%s GROUP BY DATE_FORMAT(CREATE_DATE,'%%Y-%%m-%%d');
''', firstDayOfMonth)

write(u'本月日收入信息:\n');

rows = cursor.fetchall();
totalFee = 0;
if rows:
    for row in rows:
        totalFee = totalFee + row[1]
        write(row[0] + ',' + str(row[1]) + '\n')

write(u'本月共计:' + str(totalFee) + '\n');

cursor.execute('''
    SELECT DATE_FORMAT(CREATE_DATE,'%%Y-%%m') ,SUM(REFUND_FEE+TOTAL_PAY_FEE)/100.0  FROM ARTICLE_BIZ_ORDER 
WHERE  CREATE_DATE >%s GROUP BY DATE_FORMAT(CREATE_DATE,'%%Y-%%m');
''', firstDayOfYear)

write(u'本年月收入信息:\n');

rows = cursor.fetchall();
totalFee = 0;
if rows:
    for row in rows:
        totalFee = totalFee + row[1]
        write(row[0] + ',' + str(row[1]) + '\n')

cursor.execute('''
    SELECT SUM(REFUND_FEE+TOTAL_PAY_FEE)/100.0 FROM ARTICLE_BIZ_ORDER WHERE TOTAL_PAY_FEE>0 and CREATE_DATE >%s
''', firstDayOfYear)
rows = cursor.fetchall()
if rows:
    for row in rows:
        write(u'本年共计:' + str(row[0]) + '\n')

cursor.execute('''
    SELECT SUM(REFUND_FEE+TOTAL_PAY_FEE)/100.0 FROM ARTICLE_BIZ_ORDER WHERE TOTAL_PAY_FEE>0
''')
rows = cursor.fetchall()
if rows:
    for row in rows:
        write(u'历史共计:' + str(row[0]) + '\n');

cursor.execute('''
    SELECT ARTICLE_NAME,COUNT(DISTINCT NICK) FROM ARTICLE_BIZ_ORDER WHERE CREATE_DATE>%s AND CREATE_DATE<%s group by ARTICLE_NAME
''', (yesterday, today))

write(u'----昨日新增用户数----\n')

rows = cursor.fetchall();
if rows:
    for row in rows:
        write(row[0] + ',' + str(row[1]) + '\n');

write(u'-------单个应用最近七天的付费人数------\n');
for app in allApp:
    week = (date.today() + timedelta(days= -7)).strftime("%Y%m%d")
    cursor.execute('''
        SELECT date_format(CREATE_DATE,'%%Y-%%m-%%d'),count(DISTINCT NICK) FROM ARTICLE_BIZ_ORDER WHERE TOTAL_PAY_FEE>0 AND CREATE_DATE>%s and ARTICLE_CODE=%s group by date_format(CREATE_DATE,'%%Y-%%m-%%d') 
    ''', (week, app.code))
    rows = cursor.fetchall()
    if rows:
        write(app.name + '\n')
        for row in rows:
            write(str(row[0]) + ' : ' + str(row[1]) + '\n');

#统计每个应用昨天用户登入数
write('----昨日登录用户数----\n')
for app in allApp:
    cursor2.execute('''
        SELECT COUNT(DISTINCT USER_ID) FROM ACCESS_LOG WHERE LOG_TIME>%s AND LOG_TIME<%s AND APP_KEY=%s;
    ''', (yesterday, today, app.key))
    rows = cursor2.fetchall()
    if rows:
        for row in rows:
            write(app.name + '用户数:' + str(row[0]) + '\n');                        
            
write(u'----单个应用的特别指标----\n');
cursor2.execute('''
    SELECT COUNT(DISTINCT USER_ID) FROM ACCESS_LOG WHERE URL = '/fkhb/flash/savePlacard' AND LOG_TIME>%s AND LOG_TIME<%s AND APP_KEY=12368608;
''', (yesterday, today))
rows = cursor2.fetchall()
if rows:
    for row in rows:
        write(u'昨日制作保存过海报用户数:' + str(row[0]) + '\n');

cursor2.execute('''
    SELECT COUNT(DISTINCT USER_ID) FROM ACCESS_LOG WHERE URL = '/fkbq/flash/savePic' AND LOG_TIME>%s AND LOG_TIME<%s AND APP_KEY=12368602;
''', (yesterday, today))
rows = cursor2.fetchall()
if rows:
    for row in rows:
        write(u'昨日张贴发布过标签用户数:' + str(row[0]) + '\n');
        
cursor.execute(' SELECT COUNT(*) FROM FKXN_GAME_ACTIVITY WHERE STATUS=1 ')
rows = cursor.fetchall();
if rows:
    for row in rows:
        write('疯狂小鸟当前进行中的活动数:' + str(row[0]) + '\n');
        
cursor.execute(' SELECT COUNT(*),SUM(CASE WHEN STATUS=0 THEN 1 ELSE 0 END) AS C FROM FKPM_AUTORECWINDOW ')
rows = cursor.fetchall();
if rows:
    for row in rows:
        f.write('疯狂排名自动橱窗(创建的用户数:' + str(row[0]) + '，启动的用户数' + str(row[1]) + ')\n');
            
cursor.execute(' SELECT COUNT(*),SUM(case when PLAN_STATUS=0 then 1 else 0 end) as c FROM FKPM_AUTOLISTING_PLAN ')
rows = cursor.fetchall();
if rows:
    for row in rows:
        f.write('疯狂排名自动上下架(创建的用户数:' + str(row[0]) + '，启动的用户数' + str(row[1]) + ')\n');

lz = LineZing()

f2.write(lz.main())
f.write(lz.main())
conn.close();
conn2.close();
f2.close()
f.close()
