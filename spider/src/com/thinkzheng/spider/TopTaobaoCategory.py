# -*- coding: UTF-8 -*-

'''
淘宝排行榜热词抓取，抓取分为2个过程，第一步是抓取所有的三级分类，并创建抓取任务；
第二步是抓取详细的热词，在第二步抓取过程中，如果后面还会有分页，则自动会创建一条抓取任务，直至结束。
@author: lbj
'''
from com.thinkzheng.spider.SpiderWorker import Spider, startSpider
from com.thinkzheng.spider.db.DBConnection import ConnFactorty
from pyquery.pyquery import PyQuery
import json
import re


#淘宝排行帮分类信息抓取，并创建详细的关键词抓取任务。。
class TopTaobaoCategory(Spider):
    
    def __init__(self):
        self.urlLevel3 = re.compile(r"level3=([A-Z\d_]+)")
    @staticmethod
    def name():
        return "淘宝排行榜分类"
    def checkContent(self,response):
        #淘宝网访问频繁返回的页面中包含下面的词语，所以做一下初步检测。
        return (response.find("您的访问受到限制")==-1)
        
    def onSuccess(self, tid, context, response,headers):
        #print response;
        #print response[response.find("var nav=")+8:len(response)-1]
        pictures = json.loads(response[response.find("var nav=")+8:len(response)-1]);
        #print pictures['cats']
        resp = PyQuery(pictures['cats'])
        for dl in resp.find("dl"):
            dl = PyQuery(dl)
            cate2Name = dl('dt a').text()
            for dd in dl("dd a"):
                dd = PyQuery(dd)
                url = dd.attr('href')
                m = self.urlLevel3.search(url);
                level3 = "-1";
                if(m!=None):
                    level3 = m.group(0)
                else:
                    print url;
                
                newContext = context+","+cate2Name+","+dd.text()+","+level3;
                #每一个都插入一个搜索热门，搜索上升，品牌热门，品牌上升四个关键词排行榜。
                Spider.executeSql(self,"insert into CRAWLER_TASK (task_type,url,status,http_code,task_context) values('淘宝排行帮关键词',%s,0,-1,%s)",
                                  ('http://top.taobao.com'+url+'&show=focus&up=true&offset=0',newContext))
                Spider.executeSql(self,"insert into CRAWLER_TASK (task_type,url,status,http_code,task_context) values('淘宝排行帮关键词',%s,0,-1,%s)",
                                  ('http://top.taobao.com'+url+'&show=focus&up=false&offset=0',newContext))
                Spider.executeSql(self,"insert into CRAWLER_TASK (task_type,url,status,http_code,task_context) values('淘宝排行帮关键词',%s,0,-1,%s)",
                                  ('http://top.taobao.com'+url+'&show=brand&up=true&offset=0',newContext))
                Spider.executeSql(self,"insert into CRAWLER_TASK (task_type,url,status,http_code,task_context) values('淘宝排行帮关键词',%s,0,-1,%s)",
                                  ('http://top.taobao.com'+url+'&show=brand&up=false&offset=0',newContext))
        Spider.onSuccess(self,tid, context,response,headers);

#淘宝排行榜热搜词抓取。
if __name__ == '__main__':  
    headers ={
          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
          "Cookie":"PHPSESSID=867etd7i1aa3u1hg2tp6pridn5"    
      }
    conn = ConnFactorty.getConn();
    cursor = conn.cursor();
    #准备数据，将其插入到任务表中。
    datas = (('淘宝排行榜分类','http://top.taobao.com/interface2.php?cat=TR_FS&jsv=nav',0,'服饰'),
             ('淘宝排行榜分类','http://top.taobao.com/interface2.php?cat=TR_SM&jsv=nav',0,'数码家电'),
             ('淘宝排行榜分类','http://top.taobao.com/interface2.php?cat=TR_HZP&jsv=nav',0,'化妆品'),
             ('淘宝排行榜分类','http://top.taobao.com/interface2.php?cat=TR_MY&jsv=nav',0,'母婴'),
             ('淘宝排行榜分类','http://top.taobao.com/interface2.php?cat=TR_SP&jsv=nav',0,'食品'),
             ('淘宝排行榜分类','http://top.taobao.com/interface2.php?cat=TR_WT&jsv=nav',0,'文体'),
             ('淘宝排行榜分类','http://top.taobao.com/interface2.php?cat=TR_JJ&jsv=nav',0,'家居'),
             ('淘宝排行榜分类','http://top.taobao.com/interface2.php?cat=TR_ZH&jsv=nav',0,'车|玩具|宠物|其他')
             )
    cursor.executemany('''INSERT INTO CRAWLER_TASK (TASK_TYPE,URL,STATUS,TASK_CONTEXT,HTTP_CODE) VALUES(%s,%s,%s,%s,0)''',datas);
    
    #写入获取分类信息的bbs.
    startSpider(TopTaobaoCategory,1,headers,"gbk");
