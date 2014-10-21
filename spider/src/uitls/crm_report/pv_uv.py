# -*- coding: utf8 -*-
import urllib2, urllib
import sys 
import time
from pyquery import PyQuery  as pq
from warnings import catch_warnings

reload(sys)
sys.setdefaultencoding('utf-8') #@UndefinedVariable

class LineZing():
     #print Cookie
     def __init__(self, cursor):
        self.cursor = cursor
        self.url = 'http://tongji.linezing.com'
     def login(self):
         cookies = urllib2.HTTPCookieProcessor()
         opener = urllib2.build_opener(cookies)
         urllib2.install_opener(opener)
         parms = {'username':'jekkro', 'password':'hacker', 'webname':'index', 'submit':'登录'};
         urllib2.urlopen('http://www.linezing.com/login.php', urllib.urlencode(parms));
         content = urllib2.urlopen('http://tongji.linezing.com/mystat.html').read();
         return content
         
     def update_pv_uv(self, ids):
         
         content = self.login();
         p = pq(content)
         p = p('ul').eq(0)
         
         #根据应用的个数改变而改变
         for i in range(0, 10):
             li = p('li').eq(i)
             app = li('h3')('div').eq(0)
             table = li('.data02')
             pv = table('tr').eq(3)
             appName = app.text()
             if appName != None:
                 for k in ids.keys():
                     if appName == k:
                         line = pv.text().replace('昨日', '')
                         print str(ids[k]) + k + line
                         arr = line.split(' ')
                         pv = arr[1]
                         uv = arr[2]
                         self.cursor.execute(" update CRM_REPORT set pv=%s,uv=%s where id=%s " ,
                                                (pv, uv, ids[k]))
                         break;
             else:
                  print ' 量子统计 pv uv 出现问题';
                  break;
         
     def main(self):
         pv = self.parserPv()
#lineZing = LineZing('cursor')
#lineZing.update_pv_uv()
