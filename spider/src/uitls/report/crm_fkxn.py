# -*- coding: UTF-8 -*-
from dict import fkxnApp
import sys

class CrmFkxn:
    
    tableName = fkxnApp.tableName
    article_code = fkxnApp.code
    appKey = fkxnApp.key
    
    def __init__(self, nick, cursor, sellerId='0'):
        self.nick = nick
        self.cursor = cursor
        self.sellerId = sellerId
            
    #修改活动状态
    def updateIsActivity(self):
        try:
            self.cursor.execute(' select count(*) from FKXN_GAME_ACTIVITY where status = 1 and nick = %s ', (self.nick))
            rows = self.cursor.fetchone()
            if rows != None and rows[0] != 0:
                self.cursor.execute('update ' + self.tableName + ' set is_activity=%s where seller_nick = %s ',
                         (1, self.nick))
        except:
            print 'error: update is_activity nick:' + self.nick + ',' + self.sellerId 
            print sys.exc_info()[0], sys.exc_info()[1]
   

#crmFkhb = CrmFkxn('197900695','liuyun2009313')



