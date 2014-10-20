# -*- coding:utf-8 -*
#!C:\Python27\python.exe  
''''' 
Created on 2012-12-14 
 
@author: duanzuocai 
@note: Excel 工具 
'''  
from openpyxl.cell import get_column_letter  
from openpyxl.reader.excel import load_workbook  
from openpyxl.workbook import Workbook  
from openpyxl.writer.excel import ExcelWriter  
import xlrd  
import xlwt
from csv import excel
  
class Excel2003:  
    ''''' 要安装xlrd模块 '''  
    sheet = workBook = None;  
    X = 0; Y = 0; xIndex = 0; yIndex = 0;  
      
    def __init__(self, path, sheet=0):  
        wb = xlrd.open_workbook(path)  
        sh = wb.sheet_by_index(sheet)  # sheet = wb.sheet_by_name(u'Sheet1') 得到excel.Sheet  
        self.sheet = sh  
        self.workBook = wb  
        self.Y = self.sheet.nrows  
        self.X = self.sheet.ncols
    #重新设置sheet
    def setSheet(self, sheet):
        self.sheet = self.workBook.sheet_by_index(sheet);
        self.Y = self.sheet.nrows  
        self.X = self.sheet.ncols
      
    def readLineX(self, num):  # 读一列  
        if num > self.X: return None  
        return self.sheet.col_values(num)  
    def readLineY(self, num):  # 读一排  
        if num > self.Y: return None  
        return self.sheet.row_values(num)  
      
    def read(self, x, y):  
        # 通过索引读取数据：      
        return self.sheet.cell(x, y).value  
      
    def nextY(self):  
        if self.yIndex >= self.Y: return None;  
        vs = self.readLineY(self.yIndex)  
        self.yIndex += 1;  
        return vs;  
      
    def nextX(self):  
        if self.xIndex >= self.X: return None;  
        vs = self.readLineX(self.xIndex)  
        self.xIndex += 1;  
        return vs;  
      
    def resetX(self):  
        self.xIndex = 0;  
      
    def resetY(self):  
        self.yIndex = 0;  
          
    def hasNextX(self):  
        return self.X > self.xIndex  
          
    def hasNextY(self):  
        return self.Y > self.yIndex  
      
class Excel2003Create():  
    ''''' 需要xlwt模块 '''  
    path = workBook = sheet = None;  
    def __init__(self, path):  
        self.path = path  
        self.workBook = xlwt.Workbook()  
      
    def createSheet(self, sName):  
        return self.workBook.add_sheet(sName)  
      
    def set(self, sheet_obj, x, y, value):  
        sheet_obj.write(x, y, value)  
          
    def save(self):  
        self.workBook.save(self.path)  
      
class Excel2007(Excel2003):  
    ''''' 要安装openpyxl模块 '''  
    def __init__(self, path, sheetNum):  
        wb = load_workbook(filename=path)  
        if sheetNum > len(wb.get_sheet_names()):  
            print 'Error: out of index the sheetNumber', len(wb.get_sheet_names());  
            return  
        sheetName = wb.get_sheet_names()[sheetNum]  
        self.sheet = wb.get_sheet_by_name(name=sheetName)  
        self.Y = self.sheet.get_highest_row()  
        self.X = self.sheet.get_highest_column()  
          
    def read(self, x, y):  
        return self.sheet.cell(row=y, column=x).value  
      
    def readLineX(self, num):  # 读一列  
        if num > self.X: return None  
        xs = []  
        for i in range(self.Y):  
            xs.insert(i, self.read(num, i))  
        return xs  
    def readLineY(self, num):  # 读一排  
        if num > self.Y: return None  
        ys = []  
        for i in range(self.X):  
            ys.insert(i, self.read(i, num))  
        return ys  
      
class Excel2007Write():  
    excelWriter = path = workBook = sheet = None;  
    def __init__(self, path):  
        self.path = path  
        self.workBook = Workbook()  
        self.excelWriter = ExcelWriter(workbook=self.workBook)  
      
    def createSheet(self, index, name):  
        sheet = self.workBook.worksheets[index]  
        sheet.title = name  
        return sheet  
      
    def set(self, sheet_obj, x, y, value):  
        col = get_column_letter(x + 1)  
        sheet_obj.cell('%s%s' % (col, y + 1)).value = value  
          
    def save(self):  
        self.excelWriter.save(filename=path)  
      
if __name__ == '__main__':  
    #     path = 'C:\\Users\\duanzuocai.DS\\Desktop\\ab.xlsx';  
    #           
    #     excel = Excel2007Write(path)  
    #     s1 = excel.createSheet(0, "doc1")  
    #     excel.set(s1, 0, 0, '00')  
    #     excel.set(s1, 0, 1, '01')  
    #     excel.set(s1, 0, 2, '02')  
    #     excel.set(s1, 1, 0, '10')  
    #     excel.set(s1, 1, 1, '11')  
    #     excel.save()
    
    path = '/home/liuy/download/top20w1104.xls';
    
        
     
    
