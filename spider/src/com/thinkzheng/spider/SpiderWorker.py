# -*- coding: UTF-8 -*-
'''
Created on 2011-11-25

@author: lbj

'''
from com.thinkzheng.spider.SpiderProxy import SpiderProxy
from com.thinkzheng.spider.db.DBConnection import ConnFactorty
from urllib2 import HTTPError, URLError
import sys
import threading
import time
import traceback
import urllib2

def spiderworker(mutex,headers,spider,spiderProxy,encoding="gbk"):
    waitCount = 0;
    while(True):
        conn = None;
        try:
            mutex.acquire();
            conn = ConnFactorty.getConn();
            cursor = conn.cursor();
            '''读取尚未抓取的或者失败次数小于10次的任务。'''
            sql = "SELECT T_ID,URL,TASK_CONTEXT FROM CRAWLER_TASK WHERE TASK_TYPE='"+spider.name()+"' AND (STATUS=0 or (STATUS=3 AND F_COUNT<10)) limit 0,50"
            cursor.execute(sql);
            rows = cursor.fetchall();
            #如果没有需要执行的任务，则等待10秒钟后继续。
            if(len(rows)==0):
                if(waitCount>6):
                    print '已经连续一分钟没有任务，线程退出'
                    return
                print '没有 '+spider.name()+" 相关的任务，休息10秒钟后继续检查!"
                waitCount = waitCount+1;
                time.sleep(10)
                continue
            waitCount = 0;
            sql = "UPDATE CRAWLER_TASK SET STATUS = 4 WHERE T_ID IN (0";
            for r in rows:
                sql+=",";
                sql+=str(r[0]);
            sql+=")"
            cursor.execute(sql);
        except:
            pass
        finally:
            if(conn!=None):
                conn.close()
            mutex.release();
        for r in rows:
            try:
                spider.onStart(r[0])
                stime = time.clock();
                req = urllib2.Request(url=r[1],headers=headers)
                #response = urllib2.urlopen(req,timeout=20).read().decode(encoding,'ignore')
                proxy = None;
                while(True):
                    proxy = spiderProxy.getProxy();
                    response = proxy.getOpener().open(req,None,20).read().decode(encoding,'ignore')
                    #做内容的初步检查，比如是否是错误警告页面，频繁访问警告页面等。
                    if(spider.checkContent(response)):
                        #检查通过，则继续，否则标记为该代理暂时不可用,并继续用其他代理获取页面。
                        proxy.updatespeed(time.clock() - stime);
                        break;
                    else:
                        proxy.enableProxy(False)
                spider.url = r[1]
                spider.onSuccess(r[0],r[2],response,headers);
            except HTTPError,e:
                print sys.exc_info() #print all traceback exceptions, for debugging    
                print r[0],r[1];
                spider.onError(r[0],e.code);
                if(proxy!=None):  
                    proxy.enableProxy(False)
            except URLError, e:
                print sys.exc_info() #print all traceback exceptions, for debugging    
                print r[0],r[1];
                spider.onError(r[0],600); 
                if(proxy!=None):  
                    proxy.enableProxy(False)
            except:
                tb = sys.exc_info()
                print tb;
                if(tb!=None):
                    traceback.print_tb(tb[2])
                print r[0],r[1];
                spider.onError(r[0],700);   

def startSpider(spiderClass,maxSpiderCount,headers,encoding="gbk"):
    spiderProxy = SpiderProxy()
  
    threadpool = [];
    
    g_mutex = threading.Lock()
    proxyThread = threading.Thread(target=spiderProxy.loadProxy);
    proxyThread.start()
    
    for i in range(maxSpiderCount):
        threadpool.append(
                          threading.Thread(target=spiderworker, 
                                           args=(g_mutex,  headers,spiderClass(),spiderProxy,encoding)
                                           )
                          )
        threadpool[i].start();
        time.sleep(1)
    for i in range(maxSpiderCount): 
        threading.Thread.join(threadpool[i])    
    spiderProxy.stop()     
    
    
class Spider:
    enableTaskArchieve = False;
    '''
        爬虫的基类，其他爬虫应该继承该类，并且根据需要重载onStart,onSuccess,onError方法，调用基类的相应方法可以完成数据库的更新操作。
    '''
    def __init__(self):
        self.enableTaskArchieve = False;
        #如果实例化对象是本身，那么抛出异常
        if self.__class__ == Spider:
            raise NotImplementedError("abstract")
    def onStart(self,tid):
        self.writeDB(1,tid,0,None)
    def onSuccess(self,tid,context,response,headers):
        '''http成功的响应处理方法'''
        self.writeDB(2,tid,200,response) 
    def onError(self,tid,errorCode):
        '''http失败的处理方法'''
        self.writeDB(3, tid,errorCode, None)
    
    #写入新的任务到任务列表中，有些spider需要在中途产生一些子任务，可以用这个方法。
    def insertTask(self,taskType,url,context):
        self.executeSql("""INSERT INTO CRAWLER_TASK (TASK_TYPE,URL,TASK_CONTEXT,STATUS,HTTP_CODE) VALUES(%s,%s,%s,0,0)""",(taskType,url,context))
    
    #执行一句SQL语句，已经将异常捕获,如果失败则返回False，否则返回True
    def executeSql(self,sql,params):
        conn = None;
        try:
            conn = ConnFactorty.getConn();
            cursor = conn.cursor()
            cursor.execute(sql,params)
        except:
            print sys.exc_info()[0],sys.exc_info()[1] 
            return False;   
        finally:
            if(conn!=None):
                conn.close()
        return True
    def writeDB(self,status,tid,httpStatusCode,respHtml):
        '''0:未抓取,1:正在抓取,2:抓取成功,3:失败,4:已排入队列-1:任务取消'''
        '''将当前结果写入到数据库中'''
        conn = None;
        try:
            conn = ConnFactorty.getConn();
            cursor = conn.cursor();
            #开始抓取。
            if(status==1):
                cursor.execute("""
                    update CRAWLER_TASK SET STATUS=%s,HTTP_CODE=%s where T_ID = %s
                """,(status,httpStatusCode,tid))
            #失败处理
            if(status==3):
                cursor.execute("""
                    update CRAWLER_TASK SET STATUS=%s,HTTP_CODE=%s ,F_COUNT=F_COUNT+1 where T_ID = %s
                """,(status,httpStatusCode,tid))
            #抓取成功
            if(status==2):
                if(self.enableTaskArchieve):
                    cursor.execute("""
                        INSERT INTO CRAWLER_TASK_ARC (T_ID,TASK_TYPE,URL,HTML_TEXT,STATUS,HTTP_CODE,FINISH_TIME)
                        SELECT T_ID,TASK_TYPE,URL,%s,%s,%s,now() from CRAWLER_TASK WHERE T_ID=%s
                    """,(respHtml,status,httpStatusCode,tid))
                cursor.execute("delete from CRAWLER_TASK WHERE T_ID =%s",(tid))
        except:
            #print tag
            print sys.exc_info()[0],sys.exc_info()[1]    
        finally:
            if(conn!=None):
                conn.close;