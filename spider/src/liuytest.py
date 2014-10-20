# -*- coding:utf-8 -*

import sys
import os

"""
关键词每周更新一次：

1、下载top20w关键词，下载地址：http://vdisk.weibo.com/u/1908515684
http://www.taobao.com/go/act/sale/keyword-dictionary.php?qq-pf-to=pcqq.c2c

2.执行top20w_process.py

3.生成索引文件 com.thinkz.top.fkpm.updateDataJob.CreateSearchFileJob
拷贝索引文件
/data/top/dongji/index
生成fkpm_core_keyword

4.删除服务器的表的内容更新
top20w,top_tb_keyword,fkpm_core_keyword

5.更新缓存
com\thinkz\top\fkpm\action MainAction updateWordTime

"""

sys.argv = [1, '/home/thinkz/top20w_20140916.xls']
execfile("top20w_process.py");


# os.chdir("/workspace/xbox/target/xbox")
# os.system("java -cp WEB-INF/lib/*:WEB-INF/classes com.thinkz.top.fkpm.updateDataJob.CreateSearchFileJob &")
