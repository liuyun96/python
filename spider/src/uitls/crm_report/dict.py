# -*- coding: UTF-8 -*-
class App:
    def __init__(self, name, key, tableName, code):
        self.name = name
        self.key = key
        self.code = code
        self.tableName = tableName

fkhbApp = App('疯狂海报', '12368608', 'CRM_FKHB', 'ts-14633')
fkbqApp = App('疯狂标签', '12368602', 'CRM_FKBQ', 'ts-14632')
fkxnApp = App('疯狂小鸟', '12439296', 'CRM_FKXN', 'ts-18490')
fkccApp = App('疯狂橱窗', '12327559', 'CRM_FKCC', 'ts-14085')
fkpmApp = App('疯狂排名', '12412369', 'CRM_FKPM', 'ts-29562')
fkcsApp = App('疯狂车手', '21081166', 'CRM_FKCS', 'ts-1813498')
cxydApp = App('促销有道', '12317259', 'CRM_CXYD', 'ts-1816055')

apps = [fkhbApp, fkbqApp, fkxnApp]
allApp = [fkhbApp, fkbqApp, fkxnApp,fkccApp,fkpmApp,fkcsApp,cxydApp]


