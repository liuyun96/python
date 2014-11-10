# -*- coding: utf8 -*-
# Filename: accesslog_process.py

from datetime import date,timedelta
import re
import MySQLdb
import sys

#yesterday = date.today()+timedelta(days=-1)
if len(sys.argv)==2:
    yesterday=sys.argv[1]
else:
    yesterday = (date.today()+timedelta(days=-1)).strftime("%Y%m%d")
filename = '/home/43gz/accessLogs/access_'+yesterday+'.log'
f = file(filename,"r")
nameIdPattern = re.compile(r'(\S+)\((\d+)\)')
conn = MySQLdb.connect(host='localhost', user='dongji',passwd='dongji0okm',charset = "utf8",db="dongji", use_unicode = True)
cursor = conn.cursor()
while True:
    line = f.readline()
    if len(line)==0:
        break;
    start = line.find(',')
    start = line.find(',',start+1)
    end = line.find('(',start);
    end = line.rfind(',',start,end)
    if end!=-1:
        line = line[0:start]+','+line[start+1:end].replace(',','_')+line[end:]

    try:
        lp = re.split(",",line)
        logTime= lp[0]
        ip = lp[1]
        url = lp[2]
        m = nameIdPattern.search(lp[3]);
        if m!=None:
            nickName = m.group(1)
            userId = m.group(2)
        else:
            nickName = ''
            userId='0'

        m = nameIdPattern.search(lp[4])
        if m!=None:
            shopName = m.group(1)
            shopId = m.group(2)
        else:
            shopName = ''
            shopId = '0'
        m = nameIdPattern.search(lp[5])
        if m!=None:
            appName = m.group(1)
            appKey = m.group(2)
        else:
            appName = ''
            appKey='0'
        if len(lp)==8:
            version = lp[6]
            referer = lp[7]
        else:
            version='��Ѱ�'
            referer = lp[6]
        cursor.execute('''
            insert into ACCESS_LOG(LOG_TIME,IP,URL,NICK_NAME,USER_ID,SHOP_NAME,SHOP_ID,APP_NAME,APP_KEY,VERSION,REFERER)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''',(logTime,ip,url.replace('@@@',','),nickName.replace('@@@',','),userId,shopName.replace('@@@',','),shopId,appName,appKey,version,referer.replace('@@@',',')))
    except:
        print line
        #print traceback.print_exc()
        print sys.exc_info()[0],sys.exc_info()[1]

