# -*- coding: gbk -*-
'''
Created on 2011-10-4
更新店铺源链接，通过店铺街的搜索功能实现店铺源数据的更新。
@author: lbj
'''
import urllib2
import re
from BeautifulSoup import BeautifulSoup,SoupStrainer
import MySQLdb
import urllib
import time
import sys
conn = MySQLdb.connect(host='localhost', user='root',passwd='hacker',charset = "utf8",db="tb_report", use_unicode = True)  
#获取操作游标  
conn.autocommit(True)
cursor = conn.cursor()  

headers ={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
}
#提取店铺类目
catPattern = re.compile(r'<li><a href="http://shopsearch.taobao.com/browse/shop_search.htm\?rootCat=(\d+)&amp;s=0&amp;cat=(\d+)&amp;catName=[%A-Z\d]+&amp;\S+">(.+)</a></li>');
shopIdPattern = re.compile(r'shop(\d+)\.taobao\.com')
#shopPattern = re.compile(r'<td class="thumb">.+href="(http://shop(\d+)\.taobao\.com)" title="(.+)">\S+<span>主营宝贝：</span>\S+<a.+>(.+)</a>.+<p class="nick"><a target="_blank" href="(http://rate.taobao.com/user\-rate\-\d+\.htm)">(.+)</a></p>.+data-score="([\d\.]+);[\d\.]+);[\d\.]+)">店铺动态评分',re.DOTALL)
req = urllib2.Request(
  url='http://shopsearch.taobao.com/browse/shop_search.htm',
  headers = headers
  )
response = urllib2.urlopen(req).read().decode("gbk")

locations = ['重庆','浙江','深圳','广西','宁夏','江西','青岛','南昌','郑州','福州',
'长沙','沈阳','四川','温州','大连','宁波','河北','西藏','云南','甘肃','湖南','南京',
'美国,英国,法国,瑞士,澳洲,新西兰,加拿大,奥地利,韩国,日本,德国,意大利,西班牙,俄罗斯,泰国,印度,荷兰,新加坡,其它国家,海外',
'厦门','黑龙江','新疆','哈尔滨','广东','天津','成都','内蒙古','安徽','贵州','陕西','苏州','辽宁','山西','杭州',
'香港,澳门,台湾','青海','无锡','广州','江苏','中山,珠海,佛山,惠州','福建','吉林','上海','南宁','海南',
'湖北','山东','西安','河南','常州','东莞','武汉','石家庄','济南']


for m in catPattern.finditer(response):
    cat=m.group(2)
    catName =m.group(3)
    rootCat = m.group(1)
    print cat,catName
    if cat not in ['50018963','50032886','50035966','50017708','50008907','99','40','50004958']:
        continue
 
    for location in locations:
        #忽略已经处理过的数据
        if cat=='50018963' and location in ['重庆','浙江','深圳','广西','宁夏','江西','青岛','南昌','郑州','福州',
'长沙','沈阳','四川','温州','大连','宁波','河北','西藏','云南','甘肃','湖南','南京',
'美国,英国,法国,瑞士,澳洲,新西兰,加拿大,奥地利,韩国,日本,德国,意大利,西班牙,俄罗斯,泰国,印度,荷兰,新加坡,其它国家,海外',
'厦门','黑龙江','新疆','哈尔滨','广东','天津','成都','内蒙古','安徽','贵州','陕西','苏州','辽宁','山西','杭州',
'香港,澳门,台湾','青海','无锡','广州','江苏','中山,珠海,佛山,惠州','福建','吉林','上海','南宁']:
            continue
    

        page =1
        data = {'cattype':1,
                'rootCat':rootCat,
                'cat':cat,
                'loc':location,
                'sort':'shop_renqi_desc',
                'stat':4,
                'catName':catName
                }
        totalPage = 100
        while(page<=totalPage):
            data['s'] = str((page-1)*40);
            url="http://shopsearch.taobao.com/browse/shop_search.htm?%s" % urllib.urlencode(data)
            print "正在获取获取："+catName+location+" 第"+str(page)+"/"+str(totalPage)+"页数据："+url
            req = urllib2.Request(url=url,
                                  headers=headers)
            count = 1
            while(count<10):
                try:
                    response = urllib2.urlopen(req,timeout=20).read().decode('gbk','ignore').encode('utf8')
                    break;
                except:#处理网络超时等网络原因引起的错误。
                    print sys.exc_info() #print all traceback exceptions, for debugging    
                    time.sleep(2)
                    count=count+1
            print "获取成功，开始进行分析"
            match = re.search(r'<span class="page-info">\d+/(\d+)</span>',response)
            if match!=None:
                totalPage = int(match.group(1))
            else:
                page+=1;
                continue
            shopTags = SoupStrainer('tbody')
            startTbody = response.find('<tbody>')
            endTbody = response.find('</tbody>')
            if(startTbody==-1 or endTbody==-1):
                page=totalPage+1
                break;
            tbody = BeautifulSoup(response[startTbody:endTbody+7],parseOnlyThese=shopTags).tbody
            if tbody==None:
                page=totalPage+1
                break;
            for tag in tbody.findAll("tr"):
                try:
                    td = tag.findAll("td")
                    shopUrl = td[0].div.a['href'];
                    shopIdMatch = shopIdPattern.search(shopUrl);
                    shopId = shopIdMatch.group(1)
                    shopName = td[0].div.a['title']
                    nickName = td[2].findAll("p")[1].span['data-nick']
                    #print shopId,shopName,nickName
                    if(td[0].dl.dd.a!=None):
                        zybb = td[0].dl.dd.a.contents[0]
                    area = td[3].p.contents[0]
                    dataScore = td[4].find("a",{'class':'score'})['data-score'].split(';');
                    rateUrl = td[4].find("a",{'class':'score'})['href'];
                    shopType = 1
                    if td[2].find("ins",{'class':'service-mall'})!=None:
                        shopType = 2
                    cursor.execute("""
                        INSERT INTO TB_SHOP(SHOP_ID,SID,SHOP_NAME,NICK_NAME,ZYBB,DTPF_MS,DTPF_FH,DTPF_FW,SHOP_URL,RATE_URL,AREA,SHOP_TYPE)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,(shopId,cat,shopName,nickName,zybb,dataScore[0],dataScore[1],dataScore[2],shopUrl,rateUrl,area,shopType))
                except:
                    #print tag
                    print sys.exc_info()[0],sys.exc_info()[1]             
            page+=1


       
    
        