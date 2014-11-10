# -*- coding: UTF-8 -*-
'''
Created on 2011-11-29

@author: lbj
'''
from com.thinkzheng.spider.db.DBConnection import ConnFactorty
import urllib2
import threading
import time
def proxy_speed_compare(p1,p2):
    return cmp(p1.speed,p1.speed)
class Proxy(object):
    def __init__(self,ip,port=8080):
        self.ip = ip;
        self.port = port; 
        if(ip==None):
            self.proxy_opener = urllib2.build_opener();
        else:
            proxy_handler = urllib2.ProxyHandler({"http" : 'http://'+ip+':'+str(port)})
            self.proxy_opener = urllib2.build_opener(proxy_handler)
        self.usedCount = 0;
        self.speed = 10000;
        self.startTime = time.time()
        self.enable = True
    def updatespeed(self,speed):
        self.speed = speed   
        self.usedCount+=1
    
    def enableProxy(self,enable):
        if(self.enable ==True and enable==False):
            conn = None;
            try:
                conn = ConnFactorty.getConn()
                cursor = conn.cursor();
                cursor.execute("update proxy set active =0 where ip=%s",self.ip)
            except:
                pass
            finally:
                if(conn!=None):
                    conn.close()
        self.enable = enable
 
    def isIdle(self):
        if(self.enable):
            if(time.time()==self.startTime):
                #当前时间和开始时间相等，神奇的事情发生了，没办法也返回True吧
                return True
            if(time.time()<self.startTime):
                #时间重置，则数据复位。
                self.startTime = time.time();
                self.usedCount =0
                return True;
            if(self.usedCount/(time.time() - self.startTime)<10):
                #每秒小于10次，则返回为True
                return True;
        #每秒大于10次或者代理已经被禁用，则你等下次吧。
        return False;
    
    def getOpener(self):
        return self.proxy_opener;
    
class SpiderProxy(object):
    
    def __init__(self):
        self.proxy_mutex = threading.Lock()
        self.exitThread = False
    def stop(self):
        self.exitThread = True
    '''
         爬虫专用的代理服务器切换程序，由一个单独的python程序将收集到的代理服务器放到数据库中，
    SpiderProxy每1小时自动加载一次。爬虫程序通过getProxy方法获得相关的opener，并用这个
        进行网络访问，以减少因为频繁访问而被IP阻止。
    '''
    def loadProxy(self):
        waitTime = 3600;
        while(True and self.exitThread==False):
            try:
                self.proxy_mutex.acquire();
                if(waitTime>=3600):
                    print "更新代理服务器"
                    self.defaultProxy =  Proxy(None)
                    self.proxies = [];
                    #从数据库中加载代理服务器到内存中。
                    conn = ConnFactorty.getConn()
                    cursor = conn.cursor();
                    cursor.execute("select ip,port from CRAWLER_PROXY where speed<100 and active =1")
                    rows = cursor.fetchall();
                    for r in rows:
                        self.proxies.append(Proxy(r[0],r[1]))
                    waitTime=0;
            finally:
                self.proxy_mutex.release();
            time.sleep(10);
            waitTime=waitTime+10;
    
    def getProxy(self):
        try:
            self.proxy_mutex.acquire();
            self.proxies.sort(proxy_speed_compare);
            for proxy in self.proxies:
                if(proxy.isIdle()):
                    return proxy;
            return self.defaultProxy
        finally:
            self.proxy_mutex.release();