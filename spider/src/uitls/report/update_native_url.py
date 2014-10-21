# -*- coding: UTF-8 -*-

from DBConnection import ConnFactorty
import sys

class Run:
   def main(self):
       conn = ConnFactorty.getConn()
       cursor = conn.cursor()
       cursor.execute(" select count(*) from FKBQ_ITEM_FLASH_TAG where native_url is null ")
       total = cursor.fetchone()
       pageSize = 5000
       pageNo = (int(total[0]) + pageSize - 1) / pageSize
       start = 0
       for i in range(1, pageNo + 1):
            cursor.execute(" select num_iid from FKBQ_ITEM_FLASH_TAG where native_url is null limit %s,%s", (start, pageSize))
            numIids = cursor.fetchall()
            for o in numIids:
                numIid = o[0]
                cursor.execute(" select native_url from ITEM where num_iid=%s and native_url is not null and native_url!='' group by num_iid ",(numIid))
                native_url = cursor.fetchone()
                if native_url!= None:
                    #更新native_url
                    cursor.execute(" update FKBQ_ITEM_FLASH_TAG set native_url=%s where num_iid=%s  ",(native_url,numIid))
                    
            start = pageSize * i
            print start
       
       cursor.close()
       conn.close()
run = Run()
run.main()

