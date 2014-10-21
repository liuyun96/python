# -*- coding: utf8 -*-
import urllib2
import sys 
import time
from pyquery import PyQuery  as pq
from warnings import catch_warnings

reload(sys)
sys.setdefaultencoding('utf-8') #@UndefinedVariable

class LineZing():
     global app_unitId 
     
     app_unitId = {'思正科技有限公司':'83585', '疯狂标签':'2646388', '疯狂海报':'2939129', '疯狂排名':'2775911', '疯狂橱窗':'2679444', '疯狂小鸟':'2728111'}
     
     global Cookie;
     cookieDict = ['is63mvp2n6jr9jli5j0133lkk4', '0eb74777ea7e9623dd5d0cc94b5f69c1'];
     Cookie = 'PHPSESSID=%s;lz_tongji_userinfo=%s;';
     Cookie = Cookie % tuple(cookieDict)
     #print Cookie
     def __init__(self):
        self.url = 'http://tongji.linezing.com'
        self.headers = {
            "Cookie":Cookie,
            "Referer":"http://tongji.linezing.com/mystat.html",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2"
        }
     def parserUrlFrom(self, unitId):

         reqPv = urllib2.Request(
             url=self.url + '/url.html?type=day&rapid=today&ob=pv&unit_id=' + unitId,
             headers=self.headers)
         contentPv = urllib2.urlopen(reqPv).read()
         p = pq(contentPv)('.tlists');
         line = ''
         for i in range(0, 10):
             try:
                 tr = p('tr').eq(i + 1)
                 td = tr('td').eq(0)
                 pv = tr('td').eq(1).text()
                 if i != 0 :
                     percent = tr('td').eq(2).text()
                     href = td('a').attr('href')
                     line += href + ' ' + pv + ' ' + percent 
                     line += '\n'
             except:
                 break
         return line
        
     def parserPv(self):
         req = urllib2.Request(
             url='http://tongji.linezing.com/mystat.html',
             headers=self.headers)
         content = urllib2.urlopen(req).read()
         
         p = pq(content)
         p = p('ul').eq(0)
         
         line = ' 今日     PV  UV  IP \n'
         
         for i in range(0, 9):
             li = p('li').eq(i)
             
             app = li('h3')('div').eq(0)
             
             table = li('.data02')
             pv = table('tr').eq(1)
             
             line += app.text() + ' \n';
             line += pv.text().replace('今日','') + ' \n';
          
         return line
         
     def main(self):
         content = ''
         pv = self.parserPv()
         content += pv +'\n'
         
         for app, unitId in app_unitId.items():
            #print app + ' ' + self.parserPv(unitId)
            content += '-----' + app + ' 今日量子统计-----\n'
            content += self.parserUrlFrom(unitId)
        
         return content 
lineZing = LineZing()
print lineZing.main()
