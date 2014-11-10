#encoding=utf-8
from DBConnection import ConnFactorty
from datetime import date, timedelta, datetime
import top.api
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

url = 'static.43gz.com';
appkey = '21081166';
secret = '7c477bdde5c223d94e26daeebe2b8226'
port = 80
#昨天
entTime = (date.today() + timedelta(days= -1)).strftime("%Y-%m-%d")

def getReq(name, token=None):
    req = None;
    if name == 'SimbaLoginAuthsignGetRequest':
        req = top.api.SimbaLoginAuthsignGetRequest(url, port)
    elif name == 'SimbaRptCampaignbaseGetRequest':
        req = top.api.SimbaRptCampaignbaseGetRequest(url, port)
    elif name == 'SimbaCampaignsGetRequest':
        req = top.api.SimbaCampaignsGetRequest(url, port)
    elif name == 'SimbaRptCampaigneffectGetRequest':
        req = top.api.SimbaRptCampaigneffectGetRequest(url, port)
    elif name == 'SimbaAdgroupsGetRequest':
        req = top.api.SimbaAdgroupsGetRequest(url, port)
    elif name == 'SimbaKeywordsQscoreGetRequest':
        req = top.api.SimbaKeywordsQscoreGetRequest(url, port)
    req.set_app_info(top.appinfo(appkey, secret))
    if token != None:
        req.subway_token = token
    return req

def getToken(sessionkey):
    req = getReq('SimbaLoginAuthsignGetRequest')
    try:
        resp = req.getResponse(sessionkey)
        return resp['simba_login_authsign_get_response']['subway_token']
    except Exception, e:
        print(e)
        return None

class Campaign():
    def __init__(self, cursor, sessionkey, token, maxTime, entTime, log):
        self.cursor = cursor;
        self.sessionkey = sessionkey;
        self.token = token;
        self.maxTime = maxTime;
        self.entTime = entTime;
        self.log = log;
    #推广计划报表基础数据对象
    def getCampaignbase(self, campaign_id, title):
        req = getReq('SimbaRptCampaignbaseGetRequest', self.token)
        #req.nick = "经典名表行"
        req.start_time = self.maxTime;
        req.end_time = self.entTime;
        req.search_type = "SUMMARY"
        req.source = "1"
        req.page_no = 1
        req.page_size = 500
        req.campaign_id = campaign_id
        check = True
        try:
            resp = req.getResponse(self.sessionkey)
            bases = resp['simba_rpt_campaignbase_get_response']['rpt_campaign_base_list']
            for base in bases:
                nick = base['nick']
                campaignId = base['campaignId']
                avgpos = base['avgpos']
                aclick = base['aclick']
                cpc = base['cpc']
                cost = base['cost']
                #先把string转为date
                createDate = datetime.strptime(str(base['date']), '%Y-%m-%d');
                #再格式化
                createDate = createDate.strftime('%Y%m%d');
                impressions = base['impressions'];
                #click = base['click']
                cpm = base['cpm']
                self.cursor.execute(" insert into FKCS_CAMPAIGN(nick,campaignId,title,avgpos,aclick,cpc,cost,createDate,impressions,cpm)" + 
                                    " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (nick, campaignId, title , avgpos, aclick, cpc, cost, createDate, impressions, cpm));
        except Exception, e:
            if check:
                check = False;
                self.log.writelines(str(campaign_id) + '获取推广计划报表基础数据对象出现异常\n');
                self.log.writelines(str(e) + '\n');
            return None
    #推广计划效果报表数据对象
    def getCampaigneffect(self, campaign_id):
        req = getReq('SimbaRptCampaigneffectGetRequest', self.token);
        #req.nick = "经典名表行"
        req.start_time = self.maxTime;
        req.end_time = self.entTime;
        req.search_type = "SUMMARY"
        req.source = "SUMMARY"
        req.page_no = 1
        req.page_size = 500
        req.campaign_id = campaign_id
        check = True
        try:
            resp = req.getResponse(self.sessionkey)
            bases = resp['simba_rpt_campaigneffect_get_response']['rpt_campaign_effect_list']
            for base in bases:
                favShopCount = base['favShopCount']
                directpay = base['directpay']
                indirectpay = base['indirectpay']
                favItemCount = base['favItemCount']
                indirectpaycount = base['indirectpaycount']
                directpaycount = base['directpaycount']
                self.cursor.execute(" update FKCS_CAMPAIGN set favShopCount=%s,directpay=%s,indirectpay=%s,favItemCount=%s,indirectpaycount=%s,directpaycount=%s where campaignId = %s ", (favShopCount, directpay, indirectpay, favItemCount, indirectpaycount, directpaycount, campaign_id));
        except Exception, e:
            if check:
                check = False;
                self.log.writelines(str(campaign_id) + '保存推广计划效果\n');
                self.log.writelines(str(e) + '\n');
            return None
    #批量获取推广组
    def getAdgroups(self, campaign_id):
        req = getReq('SimbaAdgroupsGetRequest', self.token);
        req.campaign_id = campaign_id
        req.page_size = 200
        req.page_no = 1
        try:
            resp = req.getResponse(self.sessionkey)
            adgroups = resp['simba_adgroups_get_response']['adgroups']['adgroup_list']['a_d_group'];
            return adgroups;
        except Exception, e:
            print e;
            self.log.writelines('批量获取推广组\n');
            self.log.writelines(str(e) + '\n');
            return None;
        
    #得到推广计划  
    def getCamp(self):
        req = getReq('SimbaCampaignsGetRequest')
        try:
            resp = req.getResponse(self.sessionkey)
            return resp['simba_campaigns_get_response']['campaigns']['campaign']
        except Exception, e:
            self.log.writelines('得到推广计划  \n');
            self.log.writelines(str(e) + '\n');
            
    #取得的关键词质量得分列表
    def getKeywords(self, adgroup_id):
        req = getReq('SimbaKeywordsQscoreGetRequest')
        req.adgroup_id = adgroup_id
        check = True;
        try:
            resp = req.getResponse(self.sessionkey)
            keywords = resp['simba_keywords_qscore_get_response']['keyword_qscore_list']['keyword_qscore']
            qscore = 0;
            for w in keywords:
                qscore += int(w['qscore'])
            qscore = qscore / len(keywords);
            return qscore;
        except Exception, e:
           if check:
               print e;
               check = False;
               self.log.writelines(str(adgroup_id) + '修改质量质量得分列表  \n');
               self.log.writelines(str(e) + '\n');
           return 0;
    def updateKeywords(self, adgroup_id, qscore):
        self.cursor.execute(' update FKCS_ADGROUP set qscore=%s where id=%s ', (qscore, adgroup_id))
    def queryAdgroups(self, campaign_id):
        self.cursor.execute(' select id,mod_time,qscore from  FKCS_ADGROUP where campaign_id=%s ', (campaign_id))
        groups = self.cursor.fetchall();
        return groups;
    def main(self):
        campDict = self.getCamp();
        if campDict != None:
            for camp in campDict:
                campaign_id = camp['campaign_id'];
                title = str(camp['title']);
                self.getCampaignbase(campaign_id, title);
                self.getCampaigneffect(campaign_id);
                check = True;
                if title.find(u'疯狂车手') != -1:
                    #只取出疯狂车手推广组
                    adgroups = self.getAdgroups(campaign_id);
                    if adgroups != None:
                        #根据推广计划id查询数据库已经存在的分组
                        groups = self.queryAdgroups(campaign_id);
                        try:
                            for g in adgroups:
                                adgroup_id = g['adgroup_id']
                                mod_time = None;
                                localQscore = 0;
                                for id in groups:
                                    if adgroup_id == id[0]:
                                        mod_time = id[1];
                                        localQscore = id[2]
                                        break
                                modified_time = str(g['modified_time']).replace('-', '').replace(':', '').replace(' ', '');
                                if mod_time == None:
                                    qscore = self.getKeywords(adgroup_id);
                                    #保存推广组
                                    self.cursor.execute(' insert into FKCS_ADGROUP(id,nick,num_iid,campaign_id,price,mod_time,qscore) ' + 
                                    ' values(%s,%s,%s,%s,%s,%s,%s) ', (g['adgroup_id'], g['nick'], g['num_iid'], g['campaign_id'], g['nonsearch_max_price'], modified_time, qscore));
                                else:
                                     qscore = self.getKeywords(adgroup_id);
                                     if int(modified_time) != int(mod_time):
                                        self.cursor.execute(' update FKCS_ADGROUP set price=%s,mod_time=%s,qscore=%s where id=%s ',
                                                            (g['nonsearch_max_price'], modified_time, qscore, g['adgroup_id'],));
                                     else:
                                        if qscore != int(localQscore):
                                            self.updateKeywords(adgroup_id, qscore)                   
                        except Exception, e:
                            if check:
                                check = False;
                                self.log.writelines('保存推广组  \n');
                                self.log.writelines(str(e) + '\n');
                                self.log.writelines('参数campaign_id:' + str(campaign_id));

def getSession(cursor):
    cursor.execute(' select SESSION,nick from FKCS_SESSION_RECORD ');
    sessions = cursor.fetchall();
    return sessions;
def writeLog(log, content):
    print content;
    log.writelines(content);
def getMaxTime(cursor, nick):
    two_month = (date.today() + timedelta(days= -1)).strftime("%Y-%m-%d")
    cursor.execute(' select max(createDate) from FKCS_CAMPAIGN where nick=%s ', (nick));
    maxTime = cursor.fetchone();
    if maxTime[0] != None:
        maxTime = datetime.strptime(str(maxTime[0]), '%Y%m%d');
        maxTime = maxTime.strftime('%Y-%m-%d');
        #如果昨天的数据已经同步了就不要同步了
        if maxTime == entTime:
            return None;
        else:
            #返回昨天
            return entTime;
    else:
        return two_month;
    
def getTotal(cursor):
    cursor.execute(' select count(*) from FKCS_SESSION_RECORD ');
    total = cursor.fetchone()
    if total[0] != None:
        return total[0];
    else:
        return 0;

if __name__ == '__main__':
    conn = ConnFactorty.getConn()
    cursor = conn.cursor();
    records = getSession(cursor);
    total = getTotal(cursor);
    log = open('log.txt', 'w');
    writeLog(log, str(date.today()) + '\n');
    writeLog(log, '总的记录条数:' + str(total) + '\n');
    #有效个数
    userTotal = 0;
    for record in records:
        #sessionkey = '6100a14b15b5d972e3cacf1b2317965ea74ab0a5a1d7f38498315415';
        nick = record[1];
        maxTime = getMaxTime(cursor, nick);
        #具体同步哪一天的数据
        #maxTime = '2012-11-01';
        #entTime = '2012-11-30';
        #只同步昨天的数据
        #maxTime = entTime
        if maxTime != None:
            sessionkey = record[0];
            token = getToken(sessionkey);
            if token != None:
                userTotal += 1;
                campaign = Campaign(cursor, sessionkey, token, maxTime, entTime, log);
                campaign.main();
        total -= 1;
        writeLog(log, '卖家:' + nick + '已经执行完成,还剩余【' + str(total) + '】没执行  \n');
    writeLog(log, '有效个数' + str(userTotal) + '\n')
    log.close();
    cursor.close();
    conn.close;
    
    
