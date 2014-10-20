# -*- coding: UTF-8 -*-

'''
淘宝排行榜热词抓取，抓取分为2个过程，第一步是抓取所有的三级分类，并创建抓取任务；
第二步是抓取详细的热词，在第二步抓取过程中，如果后面还会有分页，则自动会创建一条抓取任务，直至结束。
@author: lbj
'''
from com.thinkzheng.spider.SpiderWorker import Spider, startSpider
from pyquery.pyquery import PyQuery
import re


#获取关键字信息  
class TopTaoBaoKeyword(Spider):
    def __init__(self):
        self.digitalPattern = re.compile(r"([\d\.]+)")
        
    @staticmethod
    def name():
        return "淘宝排行帮关键词"
    def checkContent(self,response):
        #淘宝网访问频繁返回的页面中包含下面的词语，所以做一下初步检测。
        return (response.find("您的访问受到限制")==-1)
        
    def onSuccess(self, tid, context, response,headers):
        resp = PyQuery(response)
        #下一页的任务加入到任务库中。
        pageNextUrl = resp('.page-next').attr('href');
        if(pageNextUrl!=None):
            Spider.executeSql(self,"insert into CRAWLER_TASK (task_type,url,status,http_code,task_context) values('淘宝排行帮关键词',%s,0,-1,%s)",
                              (pageNextUrl,context))     
        print tid;   
        for td in resp('.textlist tr td'):
            td = PyQuery(td)
            keyword =td('td span a').text()
            print keyword
            focus =td('td span').eq(1).find('em').text();
            upSpeed = td('td span.grow').eq(0).find('em').text()#上升幅度
            m = self.digitalPattern.search(upSpeed);
            if(m!=None):
                upSpeed = m.group(0)
            upPosition = td('td span.grow').eq(1).find('em').text()#上升位置。
            m = self.digitalPattern.search(upPosition);
            if(m!=None):
                upPosition = m.group(0)
            keywordCats = context.split(",");
            CAT_ID = keywordCats[3].replace('level3=','');
            Spider.executeSql(self,'''INSERT INTO TOP_TB_KEYWORD (FIRST_CLASS,SECOND_CLASS,THIRD_CLASS,CAT_ID,KEYWORD,CLICK_COUNT,UP_SPEED,UP_POSITION)
                values(%s,%s,%s,%s,%s,%s,%s,%s)''',(keywordCats[0],keywordCats[1],keywordCats[2],CAT_ID,keyword,focus,upSpeed,upPosition))
        Spider.onSuccess(self,tid, context,response,headers);

#淘宝排行榜热搜词抓取。
if __name__ == '__main__':  
    headers ={
          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
          "Cookie":"PHPSESSID=867etd7i1aa3u1hg2tp6pridn5"    
      }
    startSpider(TopTaoBaoKeyword,1,headers,"gbk")
