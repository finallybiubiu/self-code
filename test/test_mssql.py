# -*- coding:utf-8 -*-
__author__ = 'wangtao'
import os
import sys
import pymssql

reload(sys)
sys.setdefaultencoding("utf-8")

dbhost = "localhost"
dbname = "wddy"
dbusername = "sa"
dbpasswd = "Mime123"

#conn = pymssql.connect(host="127.0.0.1",user="",password="",databse="")
conn = pymssql.connect(host=dbhost, database="crawler_db", user="sa", password="Mime123",charset='utf8')
cur = conn.cursor()
#cur.execute("insert into wdwy(name,cardid,phonenum,address) values(u'我是名字','cardid','phonenum','address')")
# 要注意提交
conn.commit()

cur.execute("select * from wdwy")
for r in cur.fetchall():
    print str(r[1])
    print "*********************************************"

cur.close()
conn.close()
