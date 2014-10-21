#-*- encoding: utf8 -*-
import os 
import time
import re
import sys
import time
import urllib2
import shlex,subprocess
watchdogfile=open('/data/logs/dongji/watchdog.txt','w')

class BaseWatchDog:
	"""
	cmdline:启动的命令行
	killfirst:是否需要先杀掉原先的进程，如果命令行没有提供杀掉原先进程的功能，建议设为true
	need_alert:当发现问题的时候并重启完毕，是否需要告警
	"""
	def __init__(self,title,cmdline,killfirst=False,need_alert=False):
		self.title = title
		self.cmdline = cmdline
		self.killfirst =killfirst
		self.need_alert = need_alert
		self.blankSplitPattern = re.compile(r'\s+')
		self.runstatus='init'
	def printlog(self,log):
		watchdogfile.write(time.strftime('%Y-%m-%d %X ', time.localtime(time.time()))+log)
		watchdogfile.write('\n')
		watchdogfile.flush()
	# 重新启动进程。
	def startme(self):
		try:
			if(self.killfirst==True and self.ps_regex!=None):
				self.killme()
                        self.printlog('正在启动命令:'+self.cmdline)
                        subprocess.call(shlex.split(self.cmdline))
                        self.printlog('结束启动命令:'+self.cmdline)
                except:
                        self.printlog('启动命令:'+self.cmdline+' 异常，请检查启动命令');
	def killme(self):
		pid = subprocess.Popen('ps aux |grep "' + self.ps_regex + '"', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout.readlines();
		if((len(pid) > 0)):
			self.printlog('正在杀掉进程：'+self.title)
			subprocess.call("kill -9 "+self.blankSplitPattern.split(pid)[1])
	def check(self):
		if(self.checkme()==False):
			if(self.runstatus=='restart'):
				self.printlog(self.title+ '重启后检测失败');
			self.runstatus='restart'
			self.startme()		
		else:
			if self.runstatus!='ok':
				self.printlog(self.title+'运行正常')
			self.runstatus='ok'
class HttpWatchDog(BaseWatchDog):
		def __init__(self, title,url,cmdline,killfirst=False,ps_regex=None,need_alert=False):
			BaseWatchDog.__init__(self,title,cmdline,killfirst,need_alert)
			self.url = url;	
		def  checkme(self):
			try:
				urllib2.socket.setdefaulttimeout(30)
				response = urllib2.urlopen(self.url)
				return True
			except Exception, e:
				self.printlog(self.title +'检查' + self.url + '异常!'+str(sys.exc_info()[0])+str(sys.exc_info()[1]));
			return False;

class ProcessWatchDog(BaseWatchDog):
	def __init__(self,title,ps_regex,cmdline,killfirst=True,need_alert=False):
		BaseWatchDog.__init__(self,title,cmdline,killfirst,need_alert)
		self.ps_regex = ps_regex
	# 通过ps命令查看进程是否存在，如果不存在则返回false
	def checkme(self):
		pid = subprocess.Popen('ps aux |grep "' + self.ps_regex + '"', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout.readlines();
		if((len(pid) <= 0)):
			self.printlog('检查' + self.title + '异常!');
		return (len(pid) > 0)		

def s11_watchdog():
	jetty9000=HttpWatchDog(title='9000端口Jetty进程',url="http://localhost:9000/dongji/index",cmdline="/data/top/dongji/service.py restart 9000")
	jetty9002=HttpWatchDog(title='9002端口Jetty进程',url="http://localhost:9002/dongji/index",cmdline="/data/top/dongji/service.py restart 9002")
	chaping = ProcessWatchDog(title="差评告警检测进程",ps_regex="[a]pp_warning.py",cmdline="python /data/top/jobs/chat/app_warning.py")
	sync = ProcessWatchDog(title="文件同步进程",ps_regex="[s]ersync2",cmdline="/home/43gz/sync/sersync2 -n 2 -d -r -o /home/43gz/sync/dongji.xml")
	alert = ProcessWatchDog(title="系统运行检测进程",ps_regex="[a]lert.py",cmdline="python /data/top/dongji/alert.py s11")
	fontService = HttpWatchDog(title='字体进程',url="http://localhost:9003/font?text=1&font=lantinghei&isColShow=false&fontsize=16",cmdline="/data/top/fkfont/fontservice.py restart 9003")
	while True:
		jetty9000.check()
		jetty9002.check()
		chaping.check()
		sync.check()
		alert.check()
		fontService.check()
		time.sleep(60)

def s12_watchdog():
	fkpmAutoListing=ProcessWatchDog(title='疯狂排名自动上下架JobV3',ps_regex='[c]om.thinkz.top.fkpm.job.FkpmAutoListingTaskJobV3',cmdline='sh /data/top/dongji/FkpmAutoListingTaskJobV3.sh')
	fkpmAutoShowcase =ProcessWatchDog(title='疯狂排名自动橱窗推荐JobV3',ps_regex='[c]om.thinkz.top.fkpm.job.FkpmAutoShowcaseTaskJobV3',cmdline='sh /data/top/dongji/FkpmAutoShowcaseTaskJobV3.sh')
	sellerJob = ProcessWatchDog(title='处理卖家登录数据Job',ps_regex='[c]om.thinkz.top.job.TransitDataJob',cmdline='sh /data/top/dongji/transitLoginData.sh')
#	paipaiSellerJob = ProcessWatchDog(title='处理拍拍卖家登录数据Job',ps_regex='[c]om.thinkz.top.paipai.job.PaipaiTransitDataJob',cmdline='sh /data/top/dongji/paipaiTransitLoginData.sh')
	zhudongNotice = ProcessWatchDog(title='主动通知进程', ps_regex='[t]opCometStream.jar',cmdline='sh /data/top/topCometStream/run.sh')
	fkcsCore = ProcessWatchDog(title='疯狂车手第一次出词', ps_regex='[F]kcsCoreJob',cmdline='sh /data/top/dongji/fkcsCore.sh')
	fkcsUpdateData = ProcessWatchDog(title='疯狂车手更新数据',ps_regex='[F]kcsUpgradeDataJob',cmdline='sh /data/top/dongji/fkcsV2Update.sh')
	alert = ProcessWatchDog(title="系统运行检测进程",ps_regex="[a]lert.py",cmdline="python /data/top/dongji/alert.py s12")
	cxydJob = ProcessWatchDog(title='jae中的促销有道的相关job',ps_regex='[c]xydjob.jar',cmdline='sh /data/top/cxydjob/run.sh')
	while True:
		fkpmAutoListing.check()
		fkpmAutoShowcase.check()
		sellerJob.check()
#		paipaiSellerJob.check()
		zhudongNotice.check()
		fkcsCore.check()
		fkcsUpdateData.check()
		alert.check()
		cxydJob.check()
		time.sleep(60)

def s13_watchdog():
	jetty9000=HttpWatchDog(title='9000端口Jetty进程',url="http://localhost:9000/dongji/index",cmdline="/data/top/dongji/service.py restart 9000")
	fkcsCore = ProcessWatchDog(title='疯狂车手第一次出词', ps_regex='[F]kcsCoreJob',cmdline='sh /data/top/dongji/fkcsCore.sh')
	fkcsUpdatePrice = ProcessWatchDog(title='疯狂车手价格更新',ps_regex='[D]oPriceChangeJob',cmdline='sh /data/top/dongji/fkcsUpgradePrice.sh')
	fkcsAddWord = ProcessWatchDog(title='疯狂车手加词',ps_regex='[D]oAddNewWordJob',cmdline='sh /data/top/dongji/fkcsAddword.sh')
	fkcsUpdateData = ProcessWatchDog(title='疯狂车手更新数据',ps_regex='[F]kcsUpgradeDataJob',cmdline='sh /data/top/dongji/fkcsV2Update.sh')
	portalCutword = ProcessWatchDog(title='python切词进程',ps_regex='[P]ortalCutword',cmdline='sh /home/43gz/startPortalCutword.sh')
	alert = ProcessWatchDog(title="系统运行检测进程",ps_regex="[a]lert.py",cmdline="python /data/top/dongji/alert.py s13")
	while True:
		jetty9000.check()
		fkcsCore.check()
		fkcsUpdatePrice.check()
		fkcsAddWord.check()
		fkcsUpdateData.check()
		portalCutword.check()
		alert.check()
		time.sleep(60)

def z1_watchdog():
	cutword = HttpWatchDog(title='python切词进程',url="http://localhost:8088/cutword?word=abc2012",killfirst=True,ps_regex="[P]ortalCutword",cmdline="startPortalCutword.sh")
	listenFkpmTo20w=ProcessWatchDog(title="top抓词进程",ps_regex="[l]istenFkpm",killfirst=True,cmdline="python /home/43gz/spider/src/listenFkpm.py")
	fontService = HttpWatchDog(title='字体进程',url="http://localhost:9003/font?text=sdfg&font=lantinghei&isColShow=false&fontsize=16",cmdline="/data/top/fkfont/fontservice.py restart 9003")
	while True:
		cutword.check()
		listenFkpmTo20w.check()
		fontService.check()
		time.sleep(60)


if __name__ == "__main__":
	if(len(sys.argv)!=2):
		print '用法:python watchdog.py <host name> \n比如: python watchdog.py s11'
		exit(1)
	if(sys.argv[1]=='s11'):
		s11_watchdog()
	if(sys.argv[1]=='s12'):
		s12_watchdog()
	if(sys.argv[1]=='s13'):
		s13_watchdog()
	if(sys.argv[1]=='z1'):
		z1_watchdog()


