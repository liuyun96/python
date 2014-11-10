# -*- coding: UTF-8 -*-

'''
Created on 2011-11-27

@author: lbj
'''
import re
from com.thinkzheng.spider.SpiderWorker import Spider, startSpider
from pyquery.pyquery import PyQuery


class ShopRateSpider(Spider):
    def __init__(self):
        #数字提取pattern，一般为冒号后紧跟一个数字的形式。
        self.digitPattern = re.compile(ur"[:：]{1}\s*([\d\.]+)",re.UNICODE)
        self.xyPattern = re.compile(r'\[\[(\d+),')
        self.zybbPattern = re.compile(ur"[:：]{1}([\u2E80-\u9FFF/]+)\s*[\d]+",re.UNICODE)
        self.nativePattern = re.compile(ur'"native":"*([\d\.]+)%*"*')
    @staticmethod
    def name():
        return "店铺信用"
    def checkContent(self,response):
        #淘宝网访问频繁返回的页面中包含下面的词语，所以做一下初步检测。
        return (response.find("您的访问受到限制")==-1)
        
    def onSuccess(self, tid, context, response,headers):
        #print "获取成功，开始进行分析"
        resp = PyQuery(response)
        shopId = resp("#J_ShopIdHidden").val();
        createShop = resp('#J_showShopStartDate').val();
        match = self.digitPattern.search(resp(".frame div")[0].text);
        if(match!=None):
            sellerCount = match.group(1);
        match = self.digitPattern.search(resp(".frame div")[2].text)
        if(match!=None):
            zyxyRatio = match.group(1)
        match = self.zybbPattern.search(resp(".frame div")[1].text)
        if(match!=None):
            zybb = match.group(1)
        else:
            zybb = ""
        match = self.digitPattern.search(resp(".sep li")[1].text)
        if(match!=None):
            buyCount = match.group(1);
        #通过ajax获取30天店内服务情况。
        monthuserid = resp('#monthuserid').val()
        userTag = resp('#userTag').val()
        isB2C = resp('#isB2C').val()
        url = "http://ratehis.taobao.com/monthServiceAjax.htm?monthuserid="+monthuserid+"&userTag="+userTag+"&isB2C="+isB2C;
        dtpfms = resp(".shop-rate ul li").eq(0)("a em").html()
        dtpffw = resp(".shop-rate ul li").eq(1)("a em").html()
        dtpffh = resp(".shop-rate ul li").eq(2)("a em").html()
        weekSell = self.xyPattern.search(resp("#J_menu_list ul li").eq(0).attr("rel")).group(1);
        monthSell = self.xyPattern.search(resp("#J_menu_list ul li").eq(1).attr("rel")).group(1);
        bnSell = self.xyPattern.search(resp("#J_menu_list ul li").eq(2).attr("rel")).group(1);
        bnqSell = self.xyPattern.search(resp("#J_menu_list ul li").eq(3).attr("rel")).group(1);
        match = self.digitPattern.search(resp("#seller-rate h4").text())
        if(match!=None):
            hpRatio = match.group(1)
        Spider.executeSql(self,"""
            UPDATE TB_SHOP SET ZYBB=%s,CREATE_SHOP=%s,SELL_COUNT=%s,BUY_COUNT=%s,DTPF_MS=%s,DTPF_FW=%s,DTPF_FH=%s
            WHERE SHOP_ID=%s
        """,(zybb,createShop,sellerCount,buyCount,dtpfms,dtpffw,dtpffh,shopId))
        Spider.executeSql(self, """
            UPDATE SHOP_RATE_DETAIL SET SELL_COUNT=%s,BUY_COUNT=%s,DTPF_MS=%s,DTPF_FW=%s,DTPF_FH=%s,
                WEEK_SELL=%s,MONTH_SELL=%s,BN_SELL=%s,BNQ_SELL=%s,HP_RATIO=%s,ZYXY_RATIO=%s 
                WHERE SHOP_ID = %s 
        """, (sellerCount,buyCount,dtpfms,dtpffw,dtpffh,weekSell,monthSell,bnSell,bnqSell,hpRatio,zyxyRatio,shopId));
        #req = urllib2.Request(url=url,
        #                  headers=headers)
        #ratehis_resp= urllib2.urlopen(req,timeout=20).read().decode("gbk",'ignore')
        #m =self.nativePattern.findall(ratehis_resp)
        #写入店铺信用详细表。
        #Spider.executeSql(self, "UPDATE SHOP_RATE_DETAIL SET TK_SPEED=%s, TK_RATIO=%s,TS_RATIO=%s,CF_COUNT=%s where SHOP_ID=%s", (m[0],m[1],m[2],m[3],context))

        Spider.onSuccess(self,tid, context,"",headers);
#店铺信用爬虫。
if __name__ == '__main__':  
    headers ={
          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
      }
    startSpider(ShopRateSpider,10,headers)
