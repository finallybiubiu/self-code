# -*- coding:utf-8 -*-
__author__ = 'wangtao'
import os
import sys
import re
from pymongo import MongoClient
from selenium import webdriver
from bs4 import  BeautifulSoup
from logging import log

reload(sys)
sys.setdefaultencoding("utf-8")

qSearch = re.compile(r"[1-9]\d*$")
qTime = re.compile(r"")


class WdwySpider:
    def __init__(self):
        self.db_mongohdl = None
        self.db_colhdl = None
        self.db_conn = None

        try:
            self.db_conn = MongoClient("127.0.0.1:27017")
            self.db_mongohdl = self.db_conn.wtdb
            self.db_colhdl = self.db_mongohdl.wdwy
        except:
            # handle the exception
            return None
        else:
            pass

    def test_tuple(self):
        tuple_var_one = (1,)
        tuple_var = (1, 2, 4, 5, 6, "end")
        print tuple_var[1]

    def save_mongo(self, name, cardid, phonenum, updatetime):
        """
        save one tuple into collections
        :param name:
        :param cardid:
        :param phonenum:
        :param updatetime:
        :return:
        """
        db_tuple = dict()
        db_tuple["name"] = name
        db_tuple["cardid"] = cardid
        db_tuple["phonenum"] = phonenum
        db_tuple["updatetime"] = updatetime
        self.db_colhdl.insert(db_tuple)

    def get_wangdaiwuyou(self):
        """
        get data from   www.wangdaiwuyou.com
        :return:
        """
        url = "http://www.wangdaiwuyou.com/wdda.asp"
        #  url = "http://localhost/wdda.html"   # test url local
        div_name = "yqsj_k"
        driver = webdriver.PhantomJS()
        driver.get(url)
        linklist = driver.find_element_by_class_name("wdzs_sz").find_elements_by_css_selector("a")
        print linklist
        # 1:get the total number
        linkstr = linklist[-1].get_attribute("href")
        page_nums = int(qSearch.search(linkstr).group())

        for page_num in range(1, page_nums):
            # get data from current page
            for pnode in driver.find_elements_by_class_name(div_name):
                try:
                    pname = pnode.find_element_by_xpath("./div[2]/div[1]/font[1]").text.decode("utf-8")  # 姓名
                    pCardid = pnode.find_element_by_xpath("./div[2]/div[2]/font[1]").text.decode("utf-8")  # 证件号
                    phonenum = pnode.find_element_by_xpath("./div[2]/div[6]").text.decode("utf-8").split("：")[1]  # 联系电话
                    updatetime = pnode.find_element_by_xpath("./div[4]/div[6]").text.decode("utf-8").split("：")[1]  #  更新时间
                    # filter the empty info
                    if pname != "":
                        self.save_mongo(pname, pCardid, phonenum, updatetime)
                except:
                    print sys.exc_info()[0],sys.exc_info()[1]
                else:
                    pass
            # reassign driver
            newurl = "%s?Page=%d" % (url, page_num + 1)
            driver.get(newurl)
            print newurl
        driver.quit()

        def except_func():
            try:
                print "i am try body"
            except:
                print "i am except body"
            else:
                pass



if __name__ == "__main__":
    print ""

