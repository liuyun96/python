# -*- coding: UTF-8 -*-
from dict import fkbqApp
import sys

class CrmFkbq:
    
    tableName = fkbqApp.tableName
    article_code = fkbqApp.code
    appKey = fkbqApp.key
    
    def __init__(self, nick, cursor, sellerId='0'):
        self.nick = nick
        self.cursor = cursor
        self.sellerId = sellerId
    
     #修改标签数量       
    def updateTagNum(self):
        try:
            self.cursor.execute('select count(*) from FKBQ_ITEM_FLASH_TAG where user_id  = ' + self.sellerId)
            rows = self.cursor.fetchone()
            if rows != None and rows[0] != 0:
                self.cursor.execute('update ' + self.tableName + ' set tag_num=%s where seller_nick = %s ',
                         (rows[0], self.nick))
        except:
            print 'error: update tag_num nick:' + self.nick + ',' + self.sellerId 
            print sys.exc_info()[0], sys.exc_info()[1]

#crmFkhb = CrmFkbq('40','liuyun2009313')



