'''
Created on 2011-12-18

@author: THINKPAD
'''
import json
import MySQLdb
pictures = json.loads('{"pictures":[{"id":"20752","image":"http:\/\/img.alimama.cn\/adbrand\/adboard\/picture\/2011-12-10\/129865060001111210113527.jpg","down_datetime":"2011-12-12 03:41:09","width":"490","height":"170","down_num":"0","show_num":"4","favorite_num":"0","insert_dt":"2011.12.12","cid":"37","title":"yad\u65d7\u8230\u5e97","seller_score":"122121","source":"\u5e97\u94fa\u8857","nick":"yad\u65d7\u8230\u5e97","type":"B","favorited":false,"zoom_width":399,"zoom_height":139,"level":14,"short_title":"yad\u65d7\u8230\u5e97"},{"id":"20751","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1C8qFXn8kXXXXXXXX.gif?noq=y","down_datetime":"2011-12-12 03:31:08","width":"490","height":"170","down_num":"0","show_num":"1","favorite_num":"0","insert_dt":"2011.12.12","cid":"14","title":"\u53c8\u89c1\u5c0f\u5915\u02d9\u65b0\u5a49\u7ea6\u4e3b\u4e49\u02d9\u6781\u81f4\u5e73\u94fa\u5973\u88c5\u5370\u8c61\u5e97(\u6bcf\u5468\u4e00\u4e09\u4e94\u4e0a\u65b0)","seller_score":"397131","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u5c0f\u5915\u6765\u4e86","type":"C","favorited":false,"zoom_width":399,"zoom_height":139,"level":15,"short_title":"\u53c8\u89c1\u5c0f\u5915\u02d9\u65b0\u5a49..."},{"id":"20750","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1NKCFXo8tXXXXXXXX.gif?noq=y","down_datetime":"2011-12-12 03:26:12","width":"490","height":"170","down_num":"0","show_num":"0","favorite_num":"0","insert_dt":"2011.12.12","cid":"1055","title":"Moonbadi-\u9999\u6e2f\u68a6\u82ad\u8482\uff08\u56fd\u9645\uff09\u5851\u8eab\u5185\u8863\u65d7\u8230\u5e97","seller_score":"105649","source":"\u6dd8\u5b9d\u9996\u9875","nick":"red_star78","type":"C","favorited":false,"zoom_width":399,"zoom_height":139,"level":14,"short_title":"Moonbadi-\u9999\u6e2f\u68a6..."},{"id":"20749","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1x7iEXnXrXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 03:16:06","width":"490","height":"170","down_num":"0","show_num":"0","favorite_num":"0","insert_dt":"2011.12.12","cid":"14","title":"\u2605\u4eb2\u4eb2\u4f60\u7684\u5c0f\u773c\u888b\uff01\u6b27\u7f8e\u98ce~\u773c\u888b\u81ea\u5236\u539f\u521b\u6f6e\u6d41\u5973\u88c5\u3013\u6bcf\u5468\u4e09\u4e0a\u65b0\u3013","seller_score":"1073278","source":"\u6dd8\u5b9d\u9996\u9875","nick":"haifenglcn","type":"C","favorited":false,"zoom_width":399,"zoom_height":139,"level":17,"short_title":"\u2605\u4eb2\u4eb2\u4f60\u7684\u5c0f\u773c..."},{"id":"20748","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1xmeEXmJwXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 03:16:06","width":"300","height":"100","down_num":"0","show_num":"0","favorite_num":"0","insert_dt":"2011.12.12","cid":"14","title":"\u82cf\u9192\u7684\u4e50\u56ed- \u8ffd\u6c42\u4f18\u96c5 \u54c1\u5473\u751f\u6d3b \u6bcf\u5468\u4e8c10:00\u4e0a\u65b0","seller_score":"140672","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u82cf\u9192\u7684\u4e50\u56ed","type":"C","favorited":false,"zoom_width":190,"zoom_height":64,"level":14,"short_title":"\u82cf\u9192\u7684\u4e50\u56ed- \u8ffd..."},{"id":"20747","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1eyGFXl0qXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 02:36:10","width":"190","height":"90","down_num":"0","show_num":"0","favorite_num":"0","insert_dt":"2011.12.12","cid":"14","title":"\u4ebf\u8054\u670d\u9970\u4e13\u8425\u5e97","seller_score":"10456","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u4ebf\u8054\u670d\u9970\u4e13\u8425\u5e97","type":"B","favorited":false,"zoom_width":190,"zoom_height":90,"level":11,"short_title":"\u4ebf\u8054\u670d\u9970\u4e13\u8425\u5e97..."},{"id":"20746","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1f7KFXX8qXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 02:31:07","width":"300","height":"100","down_num":"0","show_num":"1","favorite_num":"0","insert_dt":"2011.12.12","cid":"1056","title":"\u3010\u5e7f\u5dde\u5546\u76df\u3011\u5361\u8299\u7433\u6b63\u54c1\u4e13\u5356\u5e97","seller_score":"141747","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u5361\u8299\u7433","type":"C","favorited":false,"zoom_width":190,"zoom_height":64,"level":14,"short_title":"\u3010\u5e7f\u5dde\u5546\u76df\u3011\u5361..."},{"id":"20745","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1v4eFXeJxXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 02:26:06","width":"300","height":"100","down_num":"0","show_num":"1","favorite_num":"0","insert_dt":"2011.12.12","cid":"29","title":"\u5e08\u9053\u65d7\u8230\u5e97","seller_score":"44422","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u5e08\u9053\u65d7\u8230\u5e97","type":"B","favorited":false,"zoom_width":190,"zoom_height":64,"level":12,"short_title":"\u5e08\u9053\u65d7\u8230\u5e97"},{"id":"20744","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1r1CFXldjXXXXXXXX.gif?noq=y","down_datetime":"2011-12-12 02:21:05","width":"300","height":"100","down_num":"0","show_num":"1","favorite_num":"0","insert_dt":"2011.12.12","cid":"14","title":"\u7f8e\u4e3d\u6ce1\u6ce1 \u7b80\u68a6\u65d7\u4e0b\u4e94\u51a0\u4e13\u8425\u5e97","seller_score":"208026","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u7f8e\u4e3d\u6ce1\u6ce1-\u65f6\u5c1a\u5305\u5305","type":"C","favorited":false,"zoom_width":190,"zoom_height":64,"level":15,"short_title":"\u7f8e\u4e3d\u6ce1\u6ce1 \u7b80\u68a6\u65d7..."},{"id":"20743","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1Q.OFXk0XXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 02:21:05","width":"490","height":"170","down_num":"0","show_num":"1","favorite_num":"0","insert_dt":"2011.12.12","cid":"14","title":"\u5929\u4f7f\u4e4b\u57ce\u5973\u88c5 \u79cb\u51ac\u65b0\u6b3e\u5973\u88c5\u7fbd\u7ed2\u670d\u6bdb\u8863\u6bdb\u5462\u5927\u8863\u5916\u5957\u53d1\u5e03","seller_score":"2557274","source":"\u6dd8\u5b9d\u9996\u9875","nick":"tearing_angel","type":"C","favorited":false,"zoom_width":399,"zoom_height":139,"level":18,"short_title":"\u5929\u4f7f\u4e4b\u57ce\u5973\u88c5 \u79cb..."},{"id":"20742","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1ji5FXbJuXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 02:11:10","width":"490","height":"170","down_num":"0","show_num":"1","favorite_num":"0","insert_dt":"2011.12.12","cid":"1040","title":"inmix \u6f6e\u6d41\u773c\u955c\u7b2c\u4e00\u54c1\u724c\uff01\u5c0f\u6c34\u773c\u955c","seller_score":"46627","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u6c34\u725b\u725b2008","type":"C","favorited":false,"zoom_width":399,"zoom_height":139,"level":12,"short_title":"inmix \u6f6e\u6d41\u773c\u955c..."},{"id":"20741","image":"http:\/\/img.alimama.cn\/adbrand\/adboard\/picture\/2011-12-09\/129803170001111209025437.jpg","down_datetime":"2011-12-12 02:11:05","width":"540","height":"290","down_num":"0","show_num":"2","favorite_num":"0","insert_dt":"2011.12.12","cid":"14","title":"\u79cb\u4e4b\u97f5\u7cbe\u54c1\u7f8a\u7ed2\u5e97","seller_score":"348","source":"\u65b0\u7248\u5973\u88c5\u7c7b\u76ee\u9996\u9875","nick":"wenwen20_123","type":"C","favorited":false,"zoom_width":399,"zoom_height":215,"level":6,"short_title":"\u79cb\u4e4b\u97f5\u7cbe\u54c1\u7f8a\u7ed2..."},{"id":"20739","image":"http:\/\/img.alimama.cn\/adbrand\/adboard\/picture\/2011-12-11\/129898200001111211133015.jpg","down_datetime":"2011-12-12 01:41:12","width":"300","height":"250","down_num":"0","show_num":"2","favorite_num":"0","insert_dt":"2011.12.12","cid":"31","title":"\u9b45\u5f71\u4ed9\u8e2a \u5361\u871c\u742akamicy\u5962\u534e\u7bb1\u5305\uff0d\u6dd8\u5b9d\u603b\u5e97","seller_score":"168665","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u9b45\u5f71\u4ed9\u8e2a","type":"C","favorited":false,"zoom_width":190,"zoom_height":159,"level":14,"short_title":"\u9b45\u5f71\u4ed9\u8e2a \u5361\u871c\u742a..."},{"id":"20740","image":"http:\/\/img.alimama.cn\/adbrand\/adboard\/picture\/2011-12-11\/129898170001111211132917.jpg","down_datetime":"2011-12-12 01:46:12","width":"300","height":"250","down_num":"0","show_num":"1","favorite_num":"0","insert_dt":"2011.12.12","cid":"31","title":"\u9b45\u5f71\u4ed9\u8e2a \u5361\u871c\u742akamicy\u5962\u534e\u7bb1\u5305\uff0d\u6dd8\u5b9d\u603b\u5e97","seller_score":"168665","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u9b45\u5f71\u4ed9\u8e2a","type":"C","favorited":false,"zoom_width":190,"zoom_height":159,"level":14,"short_title":"\u9b45\u5f71\u4ed9\u8e2a \u5361\u871c\u742a..."},{"id":"20737","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1pO5FXXXpXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 01:31:51","width":"300","height":"100","down_num":"0","show_num":"1","favorite_num":"0","insert_dt":"2011.12.12","cid":"14","title":"LINDA\u81ea\u5236\u6b27\u7f8e\u8303\u2605\u7cbe\u81f4\u767d\u9886\u65f6\u5c1a\u5bb6\u2605","seller_score":"750599","source":"\u6dd8\u5b9d\u9996\u9875","nick":"linda_fashion","type":"C","favorited":false,"zoom_width":190,"zoom_height":64,"level":16,"short_title":"LINDA\u81ea\u5236\u6b27\u7f8e\u8303..."},{"id":"20738","image":"http:\/\/img.alimama.cn\/adbrand\/adboard\/picture\/2011-12-11\/129897970001111211132311.jpg","down_datetime":"2011-12-12 01:31:51","width":"300","height":"250","down_num":"0","show_num":"2","favorite_num":"0","insert_dt":"2011.12.12","cid":"31","title":"\u9b45\u5f71\u4ed9\u8e2a \u5361\u871c\u742akamicy\u5962\u534e\u7bb1\u5305\uff0d\u6dd8\u5b9d\u603b\u5e97","seller_score":"168665","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u9b45\u5f71\u4ed9\u8e2a","type":"C","favorited":false,"zoom_width":190,"zoom_height":159,"level":14,"short_title":"\u9b45\u5f71\u4ed9\u8e2a \u5361\u871c\u742a..."},{"id":"20736","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1xdKGXiBgXXXXXXXX.gif?noq=y","down_datetime":"2011-12-12 01:26:10","width":"190","height":"90","down_num":"0","show_num":"0","favorite_num":"0","insert_dt":"2011.12.12","cid":"1046","title":"\u5c0f\u72d7\u5438\u5c18\u5668\u65d7\u8230\u5e97","seller_score":"29597","source":"\u6dd8\u5b9d\u9996\u9875","nick":"tianheyi88","type":"C","favorited":false,"zoom_width":190,"zoom_height":90,"level":12,"short_title":"\u5c0f\u72d7\u5438\u5c18\u5668\u65d7\u8230..."},{"id":"20735","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1TRGFXa8hXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 01:26:10","width":"490","height":"170","down_num":"0","show_num":"3","favorite_num":"0","insert_dt":"2011.12.12","cid":"14","title":"\u866b\u7a9d\u9996\u9875-Tone elegancy \u5c0f\u866b\u7c73\u5b50","seller_score":"1091966","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u5c0f\u866b\u7c73\u5b50","type":"C","favorited":false,"zoom_width":399,"zoom_height":139,"level":17,"short_title":"\u866b\u7a9d\u9996\u9875-Tone e..."},{"id":"20734","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T19o9FXmdXXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 01:21:09","width":"190","height":"90","down_num":"0","show_num":"0","favorite_num":"0","insert_dt":"2011.12.12","cid":"1045","title":"\u5c71\u91ce\u4e50\u6d3b\u6237\u5916\u4e13\u8425\u5e97","seller_score":"82696","source":"\u6dd8\u5b9d\u9996\u9875","nick":"\u5c71\u91ce\u4e50\u6d3b\u6237\u5916\u4e13\u8425\u5e97","type":"C","favorited":false,"zoom_width":190,"zoom_height":90,"level":13,"short_title":"\u5c71\u91ce\u4e50\u6d3b\u6237\u5916\u4e13..."},{"id":"20733","image":"http:\/\/i.mmcdn.cn\/simba\/img\/T1EVqGXbpjXXXXXXXX.jpg?noq=y","down_datetime":"2011-12-12 01:21:08","width":"490","height":"170","down_num":"0","show_num":"2","favorite_num":"0","insert_dt":"2011.12.12","cid":"1082","title":"Mr.ing \u7f8a\u76ae\u5802\u978b\u795e\u5b98\u65b9\u5e97\u3010\u6dd8\u5b9d\u7537\u978b\u7b2c\u4e00\u54c1\u724c\u3011","seller_score":"454444","source":"\u6dd8\u5b9d\u9996\u9875","nick":"kingcoca7","type":"C","favorited":false,"zoom_width":399,"zoom_height":139,"level":15,"short_title":"Mr.ing \u7f8a\u76ae\u5802\u978b..."}]}');
print pictures['pictures']
conn = MySQLdb.connect(host='localhost', user='root',passwd='hacker',charset = "utf8",db="taoexad", use_unicode = True)  
conn.autocommit(True)
cursor = conn.cursor()
for pic in pictures['pictures']:
    print (int(pic['id']),pic['image'],pic['down_datetime'],int(pic['width']),int(pic['height']),int(pic['down_num']),int(pic['favorite_num']),
     str(pic['insert_dt']),int(pic['cid']),pic['title'],int(pic['seller_score']),pic['source'],pic['nick'],pic['type'],int(pic['level']))
    cursor.execute("""INSERT INTO hb_gallery (hb_id,image,
    download_time,width,height,
    down_count,favorite_count,insert_dt,
    cid,title,seller_score,source,nick,type,level) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
    (int(pic['id']),pic['image'],pic['down_datetime'],int(pic['width']),int(pic['height']),int(pic['down_num']),int(pic['favorite_num']),
     str(pic['insert_dt']),int(pic['cid']),pic['title'],int(pic['seller_score']),pic['source'],pic['nick'],pic['type'],int(pic['level'])))