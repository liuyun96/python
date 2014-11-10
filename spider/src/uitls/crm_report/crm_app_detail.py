# -*- coding: utf8 -*-
import urllib2
import sys 
import re
from pyquery import PyQuery  as pq

class AppDetail():

     def __init__(self, cursor, service_code, id):
        self.cursor = cursor
        self.id = id;
        self.service_code = service_code
        self.headers = {
            "Referer":"http://fuwu.taobao.com/",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2"
        }
     
     def parser(self):
         req = urllib2.Request(
             url='http://fuwu.taobao.com/ser/detail.htm?service_code=' + self.service_code, headers=self.headers)
         content = urllib2.urlopen(req).read().decode('utf-8', 'ignore')
         ul = pq(content)('.use-state')
         #有效评分数
         s = ''
         grade = pq(content)('.grade').text();
         if grade != None:
             s += grade + ','
         else:
             s += '0,'
         for i in range(0, 4):
              val = ul('li').eq(i)('span').eq(1);
              text = val.text();
              text = text.replace('/30天', '').replace('次', '').replace('人', '').replace(',', '');
              s += text + ',';
              
         s += str(self.id)
         #print self.service_code + '  :  ' + s 
         self.cursor.execute(" update CRM_REPORT set score=%s,valid_score=%s,pay_user=%s,free_user=%s,num_look=%s where id=%s " , (s.split(',')))
              
         
         
         
         
