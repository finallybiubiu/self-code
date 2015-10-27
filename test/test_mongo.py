# -*- coding:utf-8 -*-
from pymongo import MongoClient

mgclient = MongoClient('localhost', 27017)
db = mgclient.wtdb
pycol = db.rrfrnds
#post = {"name": "wangtao", "password": "mime123"}
print db.collection_names()

print pycol.find()

#insert test
print "insert test *******************************************"
x = {"id": 1}
pycol.insert(x)
for lnode in pycol.find():
    print lnode
#select test
print "select test *******************************************"
name = u"闫琨"

for u in pycol.find({"name": name.encode("utf8")}):
    print u

#delete test
print "delete test *******************************************"


#update test
print "update test *******************************************"