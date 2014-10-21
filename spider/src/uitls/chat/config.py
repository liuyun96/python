# -*- coding: utf8 -*-
# Filename: Config.py
import time
from KanbanClient import KanbanClient

class User(object):
    def __init__(self, nick, name, projectId, userId, awardUserId):
        self.nick = nick;
        self.name = name;
        self.projectId = projectId;
        self.userId = userId;
        self.awardUserId = awardUserId;

class Names(object):
    def __init__(self,userId,date):
        self.userId = userId;
        self.date = date;
      
u1 = Names(17,'2013-08-01');
u2 = Names(17,'2013-08-02');
u3 = Names(17,'2013-08-03');

#不同时间值班的人
ns = [u1,u2,u3];

#项目id
projectId = 1;
#添加用户id
userId = 1;

#卡片id
cardId = 4;

slp = User('slp', '船长', projectId, userId, 17);
zlm = User('zlm', '大副', projectId, userId, 17);
panlb = User('panlb', '舵手', projectId, userId,33);
liuy = User('liuy', 'Bug', projectId, userId, 21);

#每个客服对象
users = [slp, zlm,panlb];

url = 'http://p.thinkzheng.com/api/call';

fuwuUrl = 'http://fuwu.taobao.com/score/query_suggest.do?currentPage=1&fee=1&orderType=&callback=jsonp_reviews_list&service_code=';
#url = 'http://192.168.0.192:8080/api/call';

client = KanbanClient('100001', 'osn4icnp1dgwg7z6w97b0w7b33qyvqxo', url);

#需要处理的文件
p = '/data/top/chat';
#p = 'd://t';

#保存的文件
pCopy = '/data/top/chatC';
#pCopy = 'd://c';

pLog = '/data/top/jobs.log';
#pLog = 'd://jobs.log';

class Task(object):
    def add(self, remark):
        client.CreateTask(liuy.projectId, liuy.userId, cardId, liuy.awardUserId, long(time.time() * 1000), remark, 1)

