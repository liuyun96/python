# -*- coding: utf8 -*-
# Filename: Warn.py
import sys
import urllib2
import time
import json
import datetime
from datetime import date, timedelta
from DBConnection import ConnFactorty
from dict import allApp
from config import client, slp, zlm, liuy, cardId, fuwuUrl, Task, pLog
import codecs

reload(sys) 
sys.setdefaultencoding('utf-8') 

class Warn(object):
    def __init__(self, conn, app):
        self.cursor = conn.cursor();
        self.app = app;
    def checkIsAddTask(self, userNick, today):
        self.cursor.execute(''' select count(*) from COMMENTS where service_name=%s and user_nick=%s and date=%s
                            ''', (self.app.name, userNick, today))
        value = self.cursor.fetchone();
        if value[0] != 0:
            return False;
        return True;
    def save(self, userNick, score, explanation, today):
        self.cursor.execute(''' insert into COMMENTS (user_nick,service_name,score,explanation,date,status) values(%s,%s,%s,%s,%s,0)
                            ''', (userNick, self.app.name, score, explanation, today))
    def parse(self):
        reqPv = urllib2.Request(fuwuUrl + self.app.code);
        text = urllib2.urlopen(reqPv).read();
        index = text.find('"comments"');
        text = text[index + 11:];
        index = text.find(',"totalPage"');
        text = text[0:index];
        comments = json.loads(text);
        for c in comments:
           scoreDateFormat = c['scoreDateFormat'];
           avgScore = c["avgScore"];
           userNick = c["userNick"];
           explanation = c["explanation"];
           title = userNick + ' 给了  ' + self.app.name + ' 差评请及时处理,平均分' + str(avgScore) + "," + scoreDateFormat
           if avgScore < 5:
               #只算今天的差评
               print self.app.name + str(scoreDateFormat) + title
               if str(date.today()) == scoreDateFormat:
                   check = self.checkIsAddTask(userNick, scoreDateFormat);
                   if check:
                      score = 5;
                      if avgScore < 3:
                          score = 10;
                      #保存
                      self.save(userNick, avgScore, explanation, scoreDateFormat);
                      if self.app.name == '疯狂车手':
                          para = zlm;
                      else:
                          para = zlm;
                      if True:
                          #添加金币
                          res = client.CreateTask(para.projectId, para.userId, cardId, para.awardUserId, long(time.time() * 1000), title, score)
                          if res != None and res.success :
                              print self.app.name + '成功添加了告警'
                          else:
                              print '差评警告添加任务失败';
            


if __name__ == "__main__":
    while True:
        conn = ConnFactorty.getConn()
        for app in allApp:
            try:
                warn = Warn(conn, app);
                warn.parse();
            except:
                #task = Task();
                #task.add('差评警告程序出现异常及时检查');
                print sys.exc_info()[0], sys.exc_info()[1]
                break;
        conn.close();
        #停留十分钟
        time.sleep(600);


