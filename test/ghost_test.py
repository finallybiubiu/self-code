# -*- coding: utf-8 -*-
__author__ = 'wangtao'
from ghost import Ghost
import os
import sys
import urllib
import urllib2
from bs4 import BeautifulSoup
import cookielib
from sgmllib import SGMLParser

class spidder(SGMLParser):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.domain = "renren.com"
        self.ghost = Ghost()
        self.log_url = "http://www.renren.com/SysHome.do"
        self.log_auth_url = "http://www.renren.com/PLogin.do"
        self.frd_url = "http://friend.renren.com/managefriends"
        self.posttest_url = "http://localhost/print_post.php"
        self.post_data = {
                    'email': self.email,
                    'password': self.password,
                    'domain': self.domain
                    }

    def ghost_test(self):
        with self.ghost.start() as session:
            #执行一个post请求，登录页面
            page, resources = None, None
            try:
                req = urllib2.Request(self.posttest_url, urllib.urlencode(self.post_data))
                print req
                page, resources = session.open(self.posttest_url, method='post', body=req.data)
            except:
                print sys.exc_info()[0], sys.exc_info()[1]
            else:
                print "we get the string!"




if __name__ == "__main__":
    ghostspider = spidder('iceman0481@163.com', 'singleman2010')
    ghostspider.ghost_test()
