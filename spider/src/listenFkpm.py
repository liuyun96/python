#-*- coding:utf-8 -*
'''
Created on 2013-1-29

@author: joketans
'''
import redis
import sys
import threading
import re
from pyquery.pyquery import PyQuery
from com.thinkzheng.spider.SpiderWorker import Spider
import json
import logging
import os
import time
class timer(threading.Thread):
    def __init__(self, num, interval):  
        threading.Thread.__init__(self)  
        self.thread_num = num  
        self.interval = interval  
        self.thread_stop = False  
        
    def run(self): #Overwrite run() method, put what you want the thread do here  
        while(True):
            subscriberRedis()
    def stop(self):  
        self.thread_stop = True
      
def startTask(path):
    if path != 1:
        os.chdir("/home/43gz/spider/src")
        try:
            sys.argv = [1, path]        
            execfile("top20w_process.py")
        except Exception as e:
            logger.info("处理excel异常：" + str(e))    
        logger.info('开始 处理 类目词')
        try:
            execfile("com/thinkzheng/spider/TopTaobaoCategory.py")
            logger.info('开始抓取类目关键词')
            execfile("com/thinkzheng/spider/TopTaobao.py")  
            return True
        except Exception as e:  
            logger.info("爬类目词异常：" + str(e))    
        logger.info('开始处理excel path:' + path)
    return False
def scpXls(path):
    if path != 1:
        try:
            logger.info("开始复制xls")
            sys.argv = [1, path]
            os.system("/home/43gz/fkpmScpXls.sh " + path)
            logger.info("复制xls完成")
        except Exception as e:
                logger.info("复制excel异常：" + str(e))    
def subscriberRedis():
    try:
        redisclient = redis.Redis(host='localhost', port=6379, db=0)
        sub = redisclient.pubsub()
        sub.subscribe("fkpmTop20w")
        for msg in sub.listen():
            logger.info('收到信息 data:' + str(msg["data"]))
            scpXls(msg["data"])
            if startTask(msg["data"]):
                logger.info('数据更新完成通知生成索引文件程序')
                os.chdir("/home/43gz/top/dongji")
                os.system("java -cp WEB-INF/lib/*:WEB-INF/classes com.thinkz.top.fkpm.updateDataJob.CreateSearchFileJob &")
                logger.info("制作索引文件完成，开始复制索引文件")
                nowdate = time.strftime('%Y%m%d', time.localtime(time.time()))
                os.system("/home/43gz/fkpmScpIndex.sh " + nowdate)
                logger.info("复制索引文件完成")
                redisclient.set("createIndex", "f");
                redisclient.expire("createIndex", 60 * 60 * 24)
    except Exception as e:
        logger.info(str(e))

logger = logging.getLogger()
#set loghandler
logfile = logging.FileHandler("/home/43gz/listen.log")
logger.addHandler(logfile)
#set formater
#formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
logfile.setFormatter(formatter) 
#set log level
logger.setLevel(logging.NOTSET)
logger.info('疯狂排名更新监听程序')
{'re':re,
"PyQuery":PyQuery,
"Spider":Spider,
"json":json}        
thread = timer(1, 1)
thread.start();
          
