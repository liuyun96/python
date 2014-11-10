# -*- coding: UTF-8 -*-

'''
广告图片分析精灵图片信息抓取,抓取前需要往task表里插入下面的url任务：
http://taoshow.taoex.com/main/load/0_0/0/4/999999999/0/0/0/800?_=1324172736171
insert into task(TASK_TYPE,URL,STATUS) VALUES('广告图片','http://taoshow.taoex.com/main/load/0_0/0/4/999999999/0/0/0/0?_=1324172736171',0)
@author: lbj
'''
from com.thinkzheng.spider.SpiderWorker import Spider, startSpider
from com.thinkzheng.spider.db.DBConnection import DBConfig, ConnFactorty
import json


class TaoExAdImageSpider(Spider):
    def __init__(self):
        pass
    @staticmethod
    def name():
        return "广告图片"
    def checkContent(self,response):
        #淘宝网访问频繁返回的页面中包含下面的词语，所以做一下初步检测。
        return (response.find("您的访问受到限制")==-1)
        
    def onSuccess(self, tid, context, response,headers):
        print response;
        #print "获取成功，开始进行分析"
        pictures = json.loads(response);
        for pic in pictures['pictures']:
            Spider.executeSql(self,"""INSERT INTO hb_gallery (hb_id,image,
                download_time,width,height,
                down_count,favorite_count,insert_dt,
                cid,title,seller_score,source,nick,type,level) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
            (int(pic['id']),pic['image'],pic['down_datetime'],int(pic['width']),int(pic['height']),int(pic['down_num']),int(pic['favorite_num']),
            str(pic['insert_dt']),int(pic['cid']),pic['title'],int(pic['seller_score']),pic['source'],pic['nick'],pic['type'],int(pic['level'])))
        Spider.onSuccess(self,tid, context,response,headers);
#店铺信用爬虫。
if __name__ == '__main__':  
    DBConfig.host="localhost"
    DBConfig.username = "root"
    DBConfig.password = "hacker"
    DBConfig.database_name = "taoexad"
    #初始化爬虫任务。
    headers ={
          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
          "Cookie":"PHPSESSID=961ca621f21be85fec7ece672b176a51"    
      }
    conn = ConnFactorty.getConn();
    cursor = conn.cursor();
    for i in range(0,1300):
        cursor.execute("insert into task(TASK_TYPE,URL,STATUS) VALUES('广告图片','http://taoshow.taoex.com/main/load/0_0/0/4/999999999/0/0/0/"+str(i)+"?_=1324172736171',0)");
    
    startSpider(TaoExAdImageSpider,1,headers)
