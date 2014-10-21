# -*- coding: UTF-8 -*-
from crm_report import Report
#biz_type 订单类型，1=新订 2=续订 3=升级 4=后台赠送 5=后台自动续订 6=订单审核后生成订购关系（暂时用不到）
class BizOrder:
    def __init__(self, cursor, startTime, endTime, app, id):
        self.cursor = cursor;
        self.startTime = startTime;
        self.endTime = endTime;
        self.app = app;
        self.id = id;
        
    #获取新增用户数
    def new_user(self):
        self.cursor.execute('SELECT COUNT(DISTINCT NICK) FROM ARTICLE_BIZ_ORDER WHERE CREATE_DATE>%s and CREATE_DATE<%s and ARTICLE_CODE=%s ',
                        (self.startTime, self.endTime, self.app.code))
        users = self.cursor.fetchone();
        report = Report(self.cursor, 'new_user', users, self.id)
        if self.id != None:
            return report.update();
        else:
            return report.save(self.app.name, self.startTime)
    #新增付费用户
    def new_pay_user(self):
        self.cursor.execute('SELECT COUNT(DISTINCT NICK) FROM ARTICLE_BIZ_ORDER WHERE CREATE_DATE>%s and CREATE_DATE<%s and ARTICLE_CODE=%s and TOTAL_PAY_FEE>0 ',
                         (self.startTime, self.endTime, self.app.code))
        users = self.cursor.fetchone();
        report = Report(self.cursor, 'new_pay_user', users, self.id)
        return report.update()
    #新增订单
    def new_order(self):
        self.cursor.execute('SELECT COUNT(*) FROM ARTICLE_BIZ_ORDER WHERE CREATE_DATE>%s and CREATE_DATE<%s and ARTICLE_CODE=%s ',
                        (self.startTime, self.endTime, self.app.code))
        users = self.cursor.fetchone();
        report = Report(self.cursor, 'new_order', users, self.id)
        return report.update()
    #已付费订单    
    def pay_order(self):
        self.cursor.execute('SELECT COUNT(*) FROM ARTICLE_BIZ_ORDER WHERE CREATE_DATE>%s and CREATE_DATE<%s and ARTICLE_CODE=%s and TOTAL_PAY_FEE>0 ',
                         (self.startTime, self.endTime, self.app.code))
        users = self.cursor.fetchone();
        report = Report(self.cursor, 'pay_order', users, self.id)
        return report.update()
    #成交金额
    def pay(self):
        self.cursor.execute(' SELECT SUM(REFUND_FEE+TOTAL_PAY_FEE)/100.0 FROM ARTICLE_BIZ_ORDER WHERE CREATE_DATE>%s and CREATE_DATE<%s and ARTICLE_CODE=%s and TOTAL_PAY_FEE>0  ',
                        (self.startTime, self.endTime, self.app.code))
        money = self.cursor.fetchone();
        report = Report(self.cursor, 'pay', money, self.id)
        return report.update()
    #老用户下单
    def old_user_order(self):
        self.cursor.execute('SELECT COUNT(*) FROM ARTICLE_BIZ_ORDER WHERE CREATE_DATE>%s and CREATE_DATE<%s and ARTICLE_CODE=%s and biz_type!=1 and TOTAL_PAY_FEE>0',
                        (self.startTime, self.endTime, self.app.code))
        users = self.cursor.fetchone();
        report = Report(self.cursor, 'old_user_order', users, self.id)
        return report.update()
    #老用户贡献
    def old_user_pay(self):
        self.cursor.execute('SELECT SUM(REFUND_FEE+TOTAL_PAY_FEE)/100.0 FROM ARTICLE_BIZ_ORDER WHERE CREATE_DATE>%s and CREATE_DATE<%s and ARTICLE_CODE=%s and biz_type!=1 and TOTAL_PAY_FEE>0 ',
                        (self.startTime, self.endTime, self.app.code))
        users = self.cursor.fetchone();
        report = Report(self.cursor, 'old_user_pay', users, self.id)
        return report.update()
    #订购转化率
    def order_rate(self):
        self.cursor.execute(' SELECT new_user/uv FROM CRM_REPORT WHERE id=%s ',
                        (self.id))
        value = self.cursor.fetchone();
        report = Report(self.cursor, 'order_rate', value, self.id)
        return report.update()
    #付费率
    def pay_rate(self):
        self.cursor.execute(' SELECT pay_order/uv FROM CRM_REPORT WHERE id=%s ',
                        (self.id))
        value = self.cursor.fetchone();
        report = Report(self.cursor, 'pay_rate', value, self.id)
        return report.update()
    #投入产出比
    def input_output_ratio(self):
        self.cursor.execute(' SELECT pay/uv FROM CRM_REPORT WHERE id=%s ',
                        (self.id))
        value = self.cursor.fetchone();
        report = Report(self.cursor, 'input_output_ratio', value, self.id)
        return report.update()
    #客单价
    def unit_price(self):
        self.cursor.execute(' SELECT pay/new_pay_user FROM CRM_REPORT WHERE id=%s ',
                        (self.id))
        value = self.cursor.fetchone();
        report = Report(self.cursor, 'unit_price', value, self.id)
        return report.update()
    #续费率
    #当日续费率=当日续费人数/当日过期人数+当日续费人数。
    def renewr_rate(self):
        #当然过期人数
        self.cursor.execute('SELECT COUNT(DISTINCT NICK) FROM ARTICLE_BIZ_ORDER WHERE ORDER_CYCLE_END>=%s and ORDER_CYCLE_END<%s and ARTICLE_CODE=%s ',
                        (self.startTime, self.endTime, self.app.code))
        users = self.cursor.fetchone();
        
        self.cursor.execute('SELECT COUNT(DISTINCT NICK) FROM ARTICLE_BIZ_ORDER WHERE CREATE_DATE>%s and CREATE_DATE<%s and ARTICLE_CODE=%s and biz_type!=1 ',
                        (self.startTime, self.endTime, self.app.code))
        old_users = self.cursor.fetchone();
        
        if users != None and old_users != None:
            users = float(users[0])
            old_users = float(old_users[0])
            value = [0];
            if old_users != 0:
                value = old_users / (old_users + users)
                value = [value]
            report = Report(self.cursor, 'renewr_rate', value, self.id)
            return report.update()
        
        
    
    
        
        
