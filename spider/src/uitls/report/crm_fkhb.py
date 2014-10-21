# -*- coding: UTF-8 -*-
from dict import fkhbApp
import sys

class CrmFkhb:
    
    tableName = fkhbApp.tableName
    article_code = fkhbApp.code
    appKey = fkhbApp.key
    
    def __init__(self, nick, cursor, sellerId='0'):
        self.cursor = cursor
        self.nick = nick
        self.sellerId = sellerId

    #修改海报数量
    def updatePlaNum(self):
        try:
            self.cursor.execute(' select count(*) from FKHB_PLACARD where user_id  = ' + self.sellerId)
            rows = self.cursor.fetchone()
            if rows != None and rows[0] != 0:
                self.cursor.execute(' update ' + self.tableName + ' set pla_num=%s where seller_nick = %s ',
                         (rows[0], self.nick))
        except:
            print 'error: update pla_num nick:' + self.nick + ',' + self.sellerId 
            print sys.exc_info()[0], sys.exc_info()[1]
                        
#crmFkhb = CrmFkhb('40', '思正科技')



