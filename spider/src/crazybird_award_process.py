# -*- coding: utf8 -*-
'''
Created on 2012-2-26
这个小程序将卖家发布的疯狂小鸟活动展示到买家平台上，一天运行一次，由crontab进行调度。
@author: lbj
'''
import MySQLdb
import sys
#计算奖品的一个排名分数，返回一个整数型
#price:当前商品价格
#nowPrice:当前商品的促销价格
#taokeRate:店铺淘客比率
#salesCount:店铺销量 
#shopScore:店铺的主观分数，用于控制排名(0-100分)。
avgPrice=100;
def caculateScore(price,nowPrice,taokeRate,salesCount,shopScore):
    if(salesCount<500):
        shopScore=shopScore+10;
    elif(salesCount<1000):
        shopScore=shopScore+20;
    elif(salesCount<2000):
        shopScore=shopScore+30;
    elif(salesCount<4000):
        shopScore=shopScore+40;
    elif(salesCount<8000):
        shopScore=shopScore+50;
    elif(salesCount<16000):
        shopScore=shopScore+60;
    else:
        shopScore=shopScore+70;
    priceScore = (price-nowPrice)/avgPrice;
    if(priceScore>100):
        priceScore =100;
    return priceScore+shopScore;

conn = MySQLdb.connect(host='192.168.0.245', user='root',passwd='baijunli',charset = "utf8",db="dongji", use_unicode = True)  
#获取操作游标  
conn.autocommit(True)
cursor = conn.cursor()
#查询所有活动的平均价格差异额，用于归一化排名顺序，所有的价格差异转化成(0-100)
cursor.execute('''
    select avg(price-now_Price) from GIFT G,GAME_ACTIVITY GA WHERE GA.IS_SHARE = 1 and GA.ID = G.ACTIVITY_ID AND GA.STATUS = 2
''')
rows = cursor.fetchall();
avgPrice = rows[0][0];
#0：待审核，1:审核通过,2：驳回
cursor.execute('''
    select NICK,USER_ID,TAOKE,SALES,SCORE,SHOP_ID FROM SELLER_AUDIT WHERE STATUS = 1
''')
rows = cursor.fetchall()
if rows:
    print '共有:'+rows.length+'个店铺在搞疯狂小鸟的活动！\n'
    for row in rows:
        shopId = row[5]
        if(shopId==None):
            continue
        print '开始处理店铺:'+shopId+'的奖品信息!'
        try:
            #删除指定卖家的奖品池中的奖品信息。
            cursor.execute('''
                DELETE FROM GIFT_POOL WHERE NICK=%s''',row[0]);
            #查询指定卖家当前激活中的奖品信息。    
            cursor.execute('''
                SELECT G.ACTIVITY_ID,GIFT_NUM,G.NAME,PRICE,PIC_URL,LEVEL,DETAIL_URL,URL,GA.END_DATE,TYPE,NOW_PRICE,G.probability,G.ID
                FROM GIFT G ,GAME_ACTIVITY GA WHERE GA.IS_SHARE = 1 AND GA.USER_ID = %s and GA.ID = G.ACTIVITY_ID AND GA.STATUS = 2
            ''',row[1]);
        except:
            print sys.exc_info()[0],sys.exc_info()[1]
            continue
            
        giftrows = cursor.fetchall()
        if giftrows:
            for giftrow in giftrows:
                try:
                    activityId = giftrow[0];
                    giftNum = giftrow[1];
                    title = giftrow[2];
                    price = giftrow[3];
                    picUrl = giftrow[4];
                    level = giftrow[5];
                    detailUrl = giftrow[6];
                    url = giftrow[7];
                    endDate = giftrow[8];
                    giftType = giftrow[9];
                    nowPrice = giftrow[10];
                    probability = giftrow[11];
                    giftId = giftrow[12];
                    score = caculateScore(price,nowPrice,row[2],row[3],row[4]);
                    print '店铺:'+shopId+'的奖品：'+title+'评分为:'+score;
                    cursor.execute('''INSERT INTO GIFT_POOL(ID,TITLE,PRICE,PIC_URL,NUM,LEVEL,END_TIME,TYPE,STATUS,ACTIVITY_ID,NICK,NOW_PRICE,SHOP_ID,SCORE,PROBABILITY,DETAIL_URL)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,2,%s,%s,%s,%s,%s,%s,%s)''',
                        (giftId,title,price,picUrl,giftNum,level,endDate,giftType,activityId,row[0],nowPrice,shopId,score,probability,detailUrl));
                except:
                    print sys.exc_info()[0],sys.exc_info()[1]
                    continue
                    


