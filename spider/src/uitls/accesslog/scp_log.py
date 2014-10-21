#!/usr/bin/env python
#-*- coding: utf-8 -*-
from datetime import date, timedelta
import time
import datetime
import subprocess
import shlex
import urllib2
#从远程服务器拷贝文件到本地
class ScpLog:
    def call(self, sh):
        subprocess.call(sh, shell=True, stderr=subprocess.PIPE)

yesterday = (date.today() + timedelta(days= -1)).strftime("%Y%m%d")
        
scp = ScpLog();
scp.call("scp 43gz@s13:/home/43gz/accessLogs/access_" + yesterday + ".log /home/43gz/accessLogs/s13/");
