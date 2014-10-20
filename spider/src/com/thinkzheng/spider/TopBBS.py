# -*- coding: UTF-8 -*-

'''
top平台bbs信息抓取程序。
@author: lbj
'''
from com.thinkzheng.spider.SpiderWorker import Spider, startSpider
from com.thinkzheng.spider.db.DBConnection import DBConfig
from pyquery.pyquery import PyQuery
import re

#获取论坛标题。
class TopBBSList(Spider):
    def __init__(self):
        pass
    @staticmethod
    def name():
        return "topbbs列表"
    def checkContent(self,response):
        #淘宝网访问频繁返回的页面中包含下面的词语，所以做一下初步检测。
        return (response.find("您的访问受到限制")==-1)
        
    def onSuccess(self, tid, context, response,headers):
        resp = PyQuery(response)
        for h3 in resp.find("h3 a"):
            url="http://dev.open.taobao.com/bbs/"+h3.attrib['href']
            print h3.text
            Spider.executeSql(self,"insert into task (task_type,url,status,http_code,task_context) values('topbbs文章',%s,0,-1,%s)",(url,h3.text))
        Spider.onSuccess(self,tid, context,response,headers);

#获取文章内容。        
class TopBBSArticle(Spider):
    def __init__(self):
        self.datePattern = re.compile(r"(\d{8})")
        self.appNamePattern = re.compile(r'“([^"]*)”')
    @staticmethod
    def name():
        return "topbbs文章"
    def checkContent(self,response):
        #淘宝网访问频繁返回的页面中包含下面的词语，所以做一下初步检测。
        return (response.find("您的访问受到限制")==-1)
        
    def onSuccess(self, tid, context, response,headers):
        resp = PyQuery(response)
        m = self.datePattern.search(context);
        if(m!=None):
            d = m.group(0)
        else:
            d = "20111111"#如果没有日期，则缺省为一个光棍节。
        t = resp('#read_tpc').text();
        url = self.url
        Spider.executeSql(self,"insert into top_chufa (create_date,content,url) values(%s,%s,%s)",(d,t,url))
        Spider.onSuccess(self,tid, context,response,headers);


#店铺信用爬虫。
if __name__ == '__main__':  
    DBConfig.host="localhost"
    DBConfig.username = "root"
    DBConfig.password = "hacker"
    DBConfig.database_name = "taoexad"
    headers ={
          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
          "Cookie":"PHPSESSID=867etd7i1aa3u1hg2tp6pridn5"    
      }
    #startSpider(TopBBSList,1,headers,"utf8");
    startSpider(TopBBSArticle,1,headers,"utf8")
