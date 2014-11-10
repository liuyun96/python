'''
Created on 2011-12-2

@author: THINKPAD
'''
import re
itemid_file = open('items.txt')
logfiles = ["1124","1125","1126","1127","1128","1129","1130","1131","1201","1202"]
items = {}
while(True):
    line = itemid_file.readline();
    if(len(line)>0):
        items[line]='NULL'
    else:
        break
pattern = re.compile(r",(http:[\S]+\.jpg)")
for logfile in logfiles:
    f = open('item_info_2011'+logfile+".log")
    while(True):
        line = f.readline();
        if(len(line)>10):
            s = line.split(",")
            if(len(s)>11):
                itemId = s[1]
                url = s[len(s)-8]
                m = pattern.search(line)
                if(m!=None):
                    urls = m.group(1).split(",")
                    if(len(urls)>=3 and len(itemId)>5 and items[itemId]!='NULL'):
                        items[itemId] = urls[2]
        else:
            break
for item in items.keys():
    print item,items[item]            
if __name__ == '__main__':
    
    f = open('d:/a.txt')
    f2 = open('d:/b.txt','w')
    pattern = re.compile(r",(http:[\S]+\.jpg)")
    items={}
    while(True):
        line = f.readline()
        if(len(line)>10):
            s = line.split(",")
            if(len(s)>11):
                itemId = s[1]
                url = s[len(s)-8]
                m = pattern.search(line)
                if(m!=None):
                    urls = m.group(1).split(",")
                    if(len(urls)>=3 and len(itemId)>5):
                        items[itemId] = urls[2]
        else:
            break
    for itemId in items.keys():
        f2.writelines("UPDATE ITEM SET NATIVE_URL='"+items[itemId]+"' WHERE NUM_IID="+itemId+";\n")
    f.close()
    f2.close()
