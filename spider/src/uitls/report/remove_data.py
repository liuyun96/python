# -*- coding: UTF-8 -*-
import sys
from DBConnection import ConnFactorty
class RemoveData:
    def __init__(self):
        self.conn = ConnFactorty.getConn();
        self.cursor = self.conn.cursor();
    def deleteItems(self, sellerId):
         print '删除没有张贴标签的商品'
         self.cursor.execute(' delete from ITEM where NATIVE_URL is null and seller_id=%s ', (sellerId));
    def updateSeller(self, sellerId):
         print '修改卖家状态'
         self.cursor.execute(' update SELLER_INFO set status=3 where seller_id=%s ', (sellerId));
    def deleteFkhb(self, sellerId):
        cursor.execute(' select id from PLACARD where seller_id=%s ', (sellerId))
        rows = cursor.fetchall()
        for row in rows:
           pId = row[0]
           print '删除疯狂海报相关信息' + pId;
           #具体的表
           cursor.execute(' delete from SELLER_FLASH_PLACARD where PLA_ID=%s ', (pId))
           cursor.execute(' delete from ITEM_MAP_PLACARD where P_ID=%s ', (pId))
           cursor.execute(' delete from PLACARD where ID=%s ', (pId))
           
    def deleteFkxn(self, nick):
        self.cursor.execute(' select ACTIVITY_ID from FKXN_GAME_ACTIVITY where nick=%s ', (nick))
        rows = self.cursor.fetchall()
        for row in rows:
           act_id = row[0]
           print '删除疯狂小鸟相关信息' + act_id
           cursor.execute(' delete from FKXN_BUYER_GAME_TIMES where ACTIVITY_ID=%s ', (act_id))
           cursor.execute(' delete from FKXN_GAME_GIFT where ACTIVITY_ID=%s ', (act_id))
           cursor.execute(' delete from FKXN_GAME_GIFT_POOL where ACTIVITY_ID=%s ', (act_id))
           cursor.execute(' delete from FKXN_GAME_PLAY_HISTORY where ACTIVITY_ID=%s ', (act_id))
           
    def main(self):
       #查询半年未登入的用户
       self.cursor.execute(' select seller_id,nick from (select seller_id,nick,TIMESTAMPDIFF(DAY,PREV_GET_TIME,now()) as n from SELLER_INFO where seller_id>1720 ) c where n>180 ')
       sellers = self.cursor.fetchall()
       #把sql写入文件
       file = open('e:/delete.sql','w');
       for row in sellers:
           sellerId = row[0];
           nick = row[1];
           #查一下是否已经订购了高级版，是否过期
           self.cursor.execute(' select count(*) from ARTICLE_BIZ_ORDER where nick=%s and TOTAL_PAY_FEE!="0" and ORDER_CYCLE_END<now() ', (nick))
           rows = self.cursor.fetchone() 
           if rows != None and rows[0] != 0:
               continue;
           try:
               deleteItems = 'delete from ITEM where NATIVE_URL is null and seller_id='+str(sellerId)+';'
               file.write(deleteItems+'\n');
               print deleteItems
               #self.updateSeller(sellerId);
               #self.deleteItems(sellerId);
           except:
               print sys.exc_info()[0], sys.exc_info()[1]
               continue;
       file.close();  
       self.cursor.close();
       self.conn.close();
    
removeData = RemoveData();
removeData.main();


