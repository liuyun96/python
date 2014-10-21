# -*- coding: UTF-8 -*-
'''
Created on 2011-11-25

@author: THINKPAD
'''
import MySQLdb 
from DBUtils.PooledDB import PooledDB 
from _mysql_exceptions import Error
import sys
class DBConfig(object):
    """数据库配置"""
    #使用的连接接口
    dbapi = MySQLdb
    #主机ip 10.241.118.37
    host = 'localhost'
    #端口
    port = 3306
    #数据库名
    database_name = 'report'
    #用户名 report
    username = 'root'
    #密码 report12344231
    password = 'baijunli'
    #最小连接数
    mincached = 1
    #最大连接数
    maxcached = 10
    #使用unicode
    use_unicode = True
    #字符编码为utf8
    charset = "utf8"
 
class ConnFactortyReport(object):
    """
        数据库连接工厂，负责产生数据库连接 , 此类是不可以被实例化的
        获取连接对象：conn = ConnFactorty.getConn()
    """
    #连接池对象
    __pool = None
    def __init__(self):
        #如果实例化对象是本身，那么抛出异常
        if self.__class__ == ConnFactortyReport:
            raise NotImplementedError("abstract")
    @staticmethod
    def getConn():
        if ConnFactortyReport.__pool is None :
            __pool = PooledDB(creator=DBConfig.dbapi, mincached=DBConfig.mincached , maxcached=DBConfig.maxcached ,
                              host=DBConfig.host , port=DBConfig.port , user=DBConfig.username , passwd=DBConfig.password ,
                              db=DBConfig.database_name, use_unicode=DBConfig.use_unicode, charset=DBConfig.charset)
        tryCount = 0; 
        while(tryCount < 50):
            try:
                return  __pool.connection()
            except:
                print sys.exc_info()[0], sys.exc_info()[1] 
                tryCount += 1
        raise Error("数据库链接错误!");
