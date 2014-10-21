# -*- coding: utf8 -*-
# Filename: accesslog_process.py
from datetime import date, timedelta
import re
import MySQLdb
import sys
import traceback
import subprocess

reload(sys) 
sys.setdefaultencoding('utf-8') 

class ProcessLog:
    def process(self, path):
        if len(sys.argv) == 2:
            yesterday = sys.argv[1]
        else:
            yesterday = (date.today() + timedelta(days= -1)).strftime("%Y%m%d")
            subprocess.call("scp 43gz@s13:/home/43gz/accessLogs/access_" + yesterday + ".log /data/logs/accesslogs/s13/",shell=True, stderr=subprocess.PIPE);
            subprocess.call("cp /home/43gz/accessLogs/access_" + yesterday + ".log /data/logs/accesslogs/",shell=True, stderr=subprocess.PIPE);
       
        filenames = [ 'access_' + yesterday + '.log']
        for filename in filenames:
        	print filename
        	f = file(path + filename, "r")
        	nameIdPattern = re.compile(r'(\S+)\((\d+)\)')
        	conn = MySQLdb.connect(host='10.241.118.37', user='report', passwd='report12344321', charset="utf8", db="report", use_unicode=True)
        	cursor = conn.cursor()
        	while True:
        		line = f.readline()
        		if len(line) == 0:
        			break;
        		start = line.find(',')
        		start = line.find(',', start + 1)
        		end = line.find('(', start);
        		end = line.rfind(',', start, end)
        		if end != -1:
        			line = line[0:start] + ',' + line[start + 1:end].replace(',', '_') + line[end:]
        
        		#将日志分解成各个部分，并写入数据库中。
        		try:
        			lp = re.split(",", line)
        			logTime = lp[0]
        			ip = lp[1]
        			url = lp[2]
        			#下面的做了一定的容错处理
        			m = nameIdPattern.search(lp[3]);
        			if m != None:
        				nickName = m.group(1)
        				userId = m.group(2)
        			else:
        				nickName = ''
        				userId = '0'
        
        			m = nameIdPattern.search(lp[4])
        			if m != None:
        				shopName = m.group(1)
        				shopId = m.group(2)
        			else:
        				shopName = ''
        				shopId = '0'
        			m = nameIdPattern.search(lp[5])
        			if m != None:
        				appName = m.group(1)
        				appKey = m.group(2)
        			else:
        				appName = ''
        				appKey = '0'
        		#下面是为适应不同的 日志的版本而做出的处理，目前是if语句中的格式
        			if len(lp) == 8:
        				version = lp[6]
        				referer = lp[7]
        			else:
        				version = '免费版'
        				referer = lp[6]
        			cursor.execute('''
        				insert into ACCESS_LOG(LOG_TIME,IP,URL,NICK_NAME,USER_ID,SHOP_NAME,SHOP_ID,APP_NAME,APP_KEY,VERSION,REFERER)
        				VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        				''', (logTime, ip, url.replace('@@@', ',')[0:255], nickName.replace('@@@', ','), userId, shopName.replace('@@@', ','), shopId, appName, appKey, version, referer.replace('@@@', ',')[0:255]))
        		except:
        		#	print line
        			print traceback.print_exc()
        			#print sys.exc_info()[0],sys.exc_info()[1]
        		#conn.commit();
        #f = open('/home/43gz/top/report/' + yesterday + '.txt', 'a');
        conn.close();
        #f.close()
			
processLog = ProcessLog();
processLog.process('/data/logs/accesslogs/')
processLog.process('/data/logs/accesslogs/s13/')

