#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time
import subprocess
import shlex
import urllib2
# 说明应用程序所在路径
apppath = '/home/dzsw2/webapp/itvtest'
# 控制台输出路径，包括stderr
stdout_file = '/home/dzsw2/logs/itv_out.log'
# 测试uri,系统后，通过该url进行检测，如果检测失败，则超过等待次数后自动退出
test_url = '/sys_info.html'
# 检测的文本内容
check_text = 'System is ok'
# 测试等待的秒数。
test_wait_time = 60


class App:
     def __init__(self, model, port, path):
        self.model = model
        self.port = port
        self.path = path

def isServiceExist(app):
    pid = subprocess.Popen('ps aux |grep "[j]etty.port=' + app.port + '"', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout.readlines()
    return (len(pid) > 0)
def stopservice(app):
    if (isServiceExist(app) == False):
        print 'cannot find the service is running'
        return 
    print 'try to stop the service'
    subprocess.call("kill $(ps aux |grep '[j]etty.port=" + app.port + "'|awk '{print $2}')", shell=True, stderr=subprocess.PIPE)
    i = 0
    while(isServiceExist(app)):
        time.sleep(1)
        sys.stdout.write('.')
        sys.stdout.flush()
        i = i + 1
        # 如果等待时间已经超过20秒，则强制杀死进程。
        if(i >= 20):
            subprocess.call("kill -9 $(ps aux |grep '[j]etty.port=" + app.port + "'|awk '{print $2}')", shell=True)
            
    print '\nstop the service successfully!'

def startservice(app):
    if (isServiceExist(app) == True):
        print 'the service is already running on port:' + app.port
        return 
    print 'start the ITV service on port:' + app.port + ', please wait....'
    outfile = open(stdout_file, 'wb+')
    subprocess.Popen('/opt/jdk1.7.0_55/bin/java -Xms256M -Xmx512M -Djetty.port=' + app.port + ' -Drun.mode=production -Dgraceful.time=20000 -cp WEB-INF/lib/*:WEB-INF/classes com.thinkz.itv.RunServer &', shell=True, stdout=outfile, stderr=outfile, cwd=app.path)
    tryCount = 0
    while(True):
        try:
            if(tryCount > test_wait_time):
                print 'start the service failure'
                break;
            response = urllib2.urlopen('http://localhost:' + app.port + test_url).read();
            print response
            if(response.find(check_text) != -1):
                print 'start the service successfully';
                break;
        except:
            time.sleep(1)
            tryCount = tryCount + 1
            print sys.exc_info()[0]


def excute(app):
    if(sys.argv[1] == 'start'):
         startservice(app)
    elif(sys.argv[1] == 'stop'):
        stopservice(app)
    elif(sys.argv[1] == 'restart'):    
        stopservice(app)
        startservice(app) 

if(len(sys.argv) != 2):
    if(sys.argv[2] == 'nomal'):
       app = App('nomal', '9000', '/home/dzsw2/webapp/itv')
       excute(app);
    else:
       app = App('test', '9090', '/home/dzsw2/webapp/itvtest')
       excute(app);
else:
    print 'usage:  service.py <stop|start|restart> <nomal|test>'
