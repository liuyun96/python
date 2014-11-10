# -*- coding: gbk -*-
'''
Created on 2011-10-4
���µ���Դ���ӣ�ͨ�����ֵ̽���������ʵ�ֵ���Դ���ݵĸ��¡�
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
#��ȡ�����α�  
conn.autocommit(True)
cursor = conn.cursor()  

headers ={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
}
#��ȡ������Ŀ
catPattern = re.compile(r'<li><a href="http://shopsearch.taobao.com/browse/shop_search.htm\?rootCat=(\d+)&amp;s=0&amp;cat=(\d+)&amp;catName=[%A-Z\d]+&amp;\S+">(.+)</a></li>');
shopIdPattern = re.compile(r'shop(\d+)\.taobao\.com')
#shopPattern = re.compile(r'<td class="thumb">.+href="(http://shop(\d+)\.taobao\.com)" title="(.+)">\S+<span>��Ӫ������</span>\S+<a.+>(.+)</a>.+<p class="nick"><a target="_blank" href="(http://rate.taobao.com/user\-rate\-\d+\.htm)">(.+)</a></p>.+data-score="([\d\.]+);[\d\.]+);[\d\.]+)">���̶�̬����',re.DOTALL)
req = urllib2.Request(
  url='http://shopsearch.taobao.com/browse/shop_search.htm',
  headers = headers
  )
response = urllib2.urlopen(req).read().decode("gbk")

locations = ['����','�㽭','����','����','����','����','�ൺ','�ϲ�','֣��','����',
'��ɳ','����','�Ĵ�','����','����','����','�ӱ�','����','����','����','����','�Ͼ�',
'����,Ӣ��,����,��ʿ,����,������,���ô�,�µ���,����,�ձ�,�¹�,�����,������,����˹,̩��,ӡ��,����,�¼���,��������,����',
'����','������','�½�','������','�㶫','���','�ɶ�','���ɹ�','����','����','����','����','����','ɽ��','����',
'���,����,̨��','�ຣ','����','����','����','��ɽ,�麣,��ɽ,����','����','����','�Ϻ�','����','����',
'����','ɽ��','����','����','����','��ݸ','�人','ʯ��ׯ','����']


for m in catPattern.finditer(response):
    cat=m.group(2)
    catName =m.group(3)
    rootCat = m.group(1)
    print cat,catName
    if cat not in ['50018963','50032886','50035966','50017708','50008907','99','40','50004958']:
        continue
 
    for location in locations:
        #�����Ѿ������������
        if cat=='50018963' and location in ['����','�㽭','����','����','����','����','�ൺ','�ϲ�','֣��','����',
'��ɳ','����','�Ĵ�','����','����','����','�ӱ�','����','����','����','����','�Ͼ�',
'����,Ӣ��,����,��ʿ,����,������,���ô�,�µ���,����,�ձ�,�¹�,�����,������,����˹,̩��,ӡ��,����,�¼���,��������,����',
'����','������','�½�','������','�㶫','���','�ɶ�','���ɹ�','����','����','����','����','����','ɽ��','����',
'���,����,̨��','�ຣ','����','����','����','��ɽ,�麣,��ɽ,����','����','����','�Ϻ�','����']:
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
            print "���ڻ�ȡ��ȡ��"+catName+location+" ��"+str(page)+"/"+str(totalPage)+"ҳ���ݣ�"+url
            req = urllib2.Request(url=url,
                                  headers=headers)
            count = 1
            while(count<10):
                try:
                    response = urllib2.urlopen(req,timeout=20).read().decode('gbk','ignore').encode('utf8')
                    break;
                except:#�������糬ʱ������ԭ������Ĵ���
                    print sys.exc_info() #print all traceback exceptions, for debugging    
                    time.sleep(2)
                    count=count+1
            print "��ȡ�ɹ�����ʼ���з���"
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


       
    
        