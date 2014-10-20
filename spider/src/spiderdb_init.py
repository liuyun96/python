# -*- coding: utf8 -*-
import MySQLdb
conn = MySQLdb.connect(host='localhost', user='root',passwd='hacker',charset = "utf8",db="taoexad", use_unicode = True)  
#获取操作游标  
conn.autocommit(True)
cursor = conn.cursor()

 
cursor.execute("""
CREATE TABLE `task` (
  `T_ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `TASK_TYPE` varchar(32) NOT NULL,
  `URL` varchar(256) NOT NULL,
  `STATUS` int(11) NOT NULL COMMENT '0:未抓取,1:正在抓取,2:抓取成功,3:失败,-1:任务取消',
  `HTTP_CODE` int(11) NOT NULL,
  `F_COUNT` int(11) DEFAULT '0',
  `TASK_CONTEXT` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`T_ID`),
  KEY `INDEX_1` (`TASK_TYPE`,`STATUS`)
) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='数据抓取任务表，所有的爬虫通过这张表实现多任务的分配。';
""");
cursor.execute("""
CREATE TABLE `task_arc` (
  `T_ID` bigint(20) NOT NULL,
  `TASK_TYPE` varchar(32) NOT NULL,
  `URL` varchar(256) NOT NULL,
  `HTML_TEXT` text COMMENT '建议只保存需要的进一步解析的html信息',
  `STATUS` int(11) NOT NULL COMMENT '0:未抓取,1:正在抓取,2:抓取成功,3:失败,-1:任务取消',
  `HTTP_CODE` int(11) NOT NULL,
  `FINISH_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`T_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='抓取任务完成后，将归档信息写入到该表，并且删除任务表中的相应记录';
""");
cursor.execute("""
CREATE TABLE `proxy` (
  `ip` varchar(15) NOT NULL DEFAULT '',
  `port` int(6) NOT NULL DEFAULT '0',
  `proxyType` int(11) NOT NULL DEFAULT '-1',
  `status` int(11) DEFAULT '0',
  `active` int(11) DEFAULT NULL,
  `time_added` int(11) NOT NULL DEFAULT '0',
  `time_checked` int(11) DEFAULT '0',
  `time_used` int(11) DEFAULT '0',
  `speed` float DEFAULT NULL,
  `area` varchar(120) DEFAULT '--',
  PRIMARY KEY (`ip`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
""")

cursor.execute("""
CREATE TABLE `hb_gallery` (
  `hb_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `image` varchar(256) DEFAULT NULL,
  `download_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `down_count` int(11) DEFAULT NULL,
  `favorite_count` int(11) DEFAULT NULL,
  `insert_dt` varchar(12) DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  `title` varchar(128) DEFAULT NULL,
  `seller_score` int(11) DEFAULT NULL,
  `source` varchar(32) DEFAULT NULL,
  `nick` varchar(64) DEFAULT NULL,
  `type` char(1) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  PRIMARY KEY (`hb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
""")

for i in range(0,656):
    url = 'http://taoshow.taoex.com/main/load/0_0/0/4/999999999/0/0/0/'+str(i)+'?_=1324172736171'
    cursor.execute("""insert into task (task_type,url,status,HTTP_CODE) values('广告图片',%s,0,-1)""",(url))
conn.commit()