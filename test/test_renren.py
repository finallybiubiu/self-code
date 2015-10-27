# -*- coding:utf-8 -*-
__author__ = 'wangtao'
from sgmllib import SGMLParser
import sys
import urllib2
import urllib
import cookielib
import os
from ghost import Ghost
from bs4 import BeautifulSoup
import re
import subprocess
import json
from pymongo import MongoClient


reload(sys)
sys.setdefaultencoding('utf8')


class spider(SGMLParser):
    def __init__(self, email, password):
        SGMLParser.__init__(self)
        self.h3 = False
        self.h3_is_ready = False
        self.div = False
        self.h3_and_div = False
        self.a = False
        self.depth = 0
        self.names = ""
        self.dic = {}

        self.email = email
        self.password = password
        self.domain = 'renren.com'
        self.file = None
        self.friend_file = None
        self.ghost = Ghost()
        self.cookie = None
        self.group_url = "http://friend.renren.com/groupsdata"
        self.group_home = "http://friend.renren.com/managefriends"
        self.file_url = "renren_cookie.txt"

        self.mongodb = MongoClient("127.0.0.1", 27017)


        try:
            self.cookie = cookielib.LWPCookieJar(self.file_url)
            cookieProc = urllib2.HTTPCookieProcessor(self.cookie)
        except:
            raise
        else:
            opener = urllib2.build_opener(cookieProc)
            urllib2.install_opener(opener)

        print "init finished successfully!!"

    def login(self):
        url = "http://www.renren.com/PLogin.do"
        group_url = "http://friend.renren.com/groupsdata"
        postdata = {
                    'email': self.email,
                    'password': self.password,
                    'domain': self.domain
                    }
        req = urllib2.Request(url, urllib.urlencode(postdata))
        self.file = urllib2.urlopen(req).read()
        self.cookie.save(self.file_url)
        """
        print "printcookie start ###################################################################"
        for cj in self.cookie:
            print cj
        print "printcookie end ###################################################################"
        """

        fp = open("test.txt", "w")
        fp.write(self.file)
        fp.close()
        #self.start_h3(None)
        #self.get_dom()
        print "getfriends*****************************************************"
        self.getfriends()
        #self.save_friends()




    def start_h3(self,attrs):
        self.h3 = True

    def end_h3(self):
        self.h3 = False
        self.h3_is_ready = True

    def start_a(self,attrs):
        if self.h3 or self.div:
            self.a = True

    def end_a(self):
        self.a = False

    def start_div(self, attrs):

        if not self.h3_is_ready:
            return

        if self.div:
            self.depth += 1

        for k,v in attrs:
            if k == 'class' and v == 'content':
                self.div = True;
                self.h3_and_div = True

    def end_div(self):
        if self.depth == 0:
            self.div = False
            self.h3_and_div = False
            self.h3_is_ready = False
            self.names = ""

        if self.div:
            self.depth -= 1

    def handle_data(self, text):
        #print "i am into handle_data"
        self.getfriends()
        if self.h3 and self.a:
            self.names += text
        if self.h3 and (not self.a):
            if not text:
                pass
            else:
                self.dic.setdefault(self.names, []).append(text)
            return
        if self.h3_and_div:
            self.dic.setdefault(self.names, []).append(text)


    def show(self):
        codetype = sys.getfilesystemencoding()
        fp_news = None
        for key in self.dic:
            str_news = ((''.join(key)).replace(' ', '')).decode('utf-8').encode(codetype),\
                ((''.join(self.dic[key])).replace(' ', '')).decode('utf-8').encode(codetype)
            print str_news
            fp_news = open("news.txt", "a+")
            fp_news.writelines(str(str_news))
            fp_news.close()


    def getfriends(self):
        all_friends_url = "http://friend.renren.com/managefriends"
        postdata = ""
        with self.ghost.start() as session:
            session.load_cookies(self.file_url)
            page, resources = None, None
            try:
                page, resources = session.open(all_friends_url)
                session.wait_for_page_loaded()
            except:
                print sys.exc_info()[0], sys.exc_info()[1]
                return
            else:
                assert page and page.http_status == 200
                print page.content

        return



    def mongo_save_friends(self,name,info):
        """
        save name info in one item
        :param name:
        :param info:
        :return:
        """
        print "mongo_save_friends"
        db = self.mongodb.wtdb
        tbl = db.rrfrnds
        frnd_dict = dict()
        db.rrfrnds.insert({"name": name, "info": info})


    def save_friends(self):
        frnds_data = urllib2.urlopen(self.group_url).read()
        frnds_json = frnds_data.split("\"data\" : ")[1]
        print "save_friends********************************************************"
        print frnds_json
        real_json = frnds_json

        real_json = real_json[:-3]
        print real_json
        real_json = json.loads(str(real_json))
        print "real_json*****************************************************************"
        #print real_json.decode("GBK")

        print real_json
        print real_json.keys()

        for frnd in real_json["friends"]:
            #print frnd["fid"], frnd["timepos"]
            fname = frnd["fname"].decode("utf8")
            finfo = frnd["info"].decode("utf8")
            print fname, finfo
            self.mongo_save_friends(frnd["fname"].decode("utf8"), frnd["info"].decode("utf8"))
            #深入下一层，获取好友的好友。



def renren_test():
    renrenspider = spider('iceman0481@163.com', 'singleman2010')
    renrenspider.login()

    #renrenspider.mongo_save_friends()

if __name__ == "__main__":
    renren_test()
    #ghost_test()

