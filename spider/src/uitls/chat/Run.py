# -*- coding: utf8 -*-
# Filename: Run.py
import MySQLdb
import sys
import codecs
import time
import datetime
import os
import shutil
from DBConnection import ConnFactorty
from chat import Chat;
from total import Total;
from config import client, users, p, pCopy, liuy, Task,ns; 

reload(sys) 
sys.setdefaultencoding('utf-8') 

class Run(object):
    #同步文件数据
    def sycnData(self):
        for item in os.listdir(p):
            d = item[0:8]
            
            itemsrc = os.path.join(p, item)
            
            conn = ConnFactorty.getConn()
            chat = Chat(conn);
            user = chat.saveReport(itemsrc);
            conn.close();
            
            conn = ConnFactorty.getConn()
            chat = Chat(conn);
            chat.total(user, d);   
            conn.close();
            
            if True:
                if user == '大副':
                    item = item.replace('_zlm', '').replace('.mht', '_zlm.mht')
                elif user == '船长':
                    item = item.replace('_slp', '').replace('.mht', '_slp.mht')
                elif user == '舵手':
                    item = item.replace('_panlb', '').replace('.mht', '_panlb.mht')
                #拷贝文件
                if user != '':
                    shutil.copy(itemsrc, pCopy + '/' + item);
                    print itemsrc + '处理完成'
                    #删除一个月前数据
                    conn = ConnFactorty.getConn()
                    chat = Chat(conn);
                    #chat.deleteData();
                if os.path.isfile(itemsrc): 
                    os.remove(itemsrc)
    #计算同步数据
    def jsData(self):
        task = Task();
        for para in users:
                conn = ConnFactorty.getConn();
                #调试status
                total = Total(conn, 0);
                results = total.getDates(para.name);
                for d in results:
                    d = d[0];
                    dict = None;
                    if para.name == '船长':
                        dict = total.zhiTC(para, d);
                    else:
                        dict = total.keFu(para, d);
                    value = dict['value'];
                    if value != None and value >= 0:
                        remark = str(d) + dict['remark'];
                        print para.name + remark + ' [总金币: ' + str(value) + ']';
                        if True:
                            #添加金币
                            userId = para.userId
                            for n in ns:
                                if d == n.date:
                                    userId = n.userId;
                                    print '更改了用户ID'+userId;
                                    break;
                            res = client.AddAwardPoint(para.projectId, userId, para.awardUserId, remark , value)
                            if res != None and res.success :
                                #修改已经添加过金币的状态
                                total.updateStatus(para, d);
                                print para.nick + ' add ' + str(value) + ' point ';
                            else:
                                task.add('调用添加金币接口发生错误');
                                break;
                    else:
                        total.updateStatus(para, d);
                conn.close();
    def main(self):
        self.sycnData();
        self.jsData();
run = Run()
run.main()
