# -*- coding: UTF-8 -*-
class Report:
    def __init__(self, cursor, column, value, id):
        self.cursor = cursor
        self.column = column
        if value != None:
            if len(value) == 1:
                self.value = value[0]
            else:
                self.value = value
        else:
            self.value = 0;   
        self.id = id
        
        
    #更新报表单个字段数据
    def update(self):
         if self.id != None:
              self.cursor.execute(" update CRM_REPORT set " + self.column + "=%s where id=%s " ,
                                        (self.value, self.id))
         return self.value;
    #保存报表数据
    def save(self, appName, createDate):
        if self.id == None:
               self.cursor.execute(" insert into CRM_REPORT (create_date,app_name," + self.column + ") values (%s,%s,%s) ",
                 (createDate, appName, self.value))
        return self.value;
    
    def simple_column(self):
        self.cursor.execute('SELECT  ' + self.column + ' from CRM_REPORT WHERE id=%s ',
                         (self.id))
        value = self.cursor.fetchone();
        if value != None:
            return value[0];
        return 0;
        
            
            
        
        
