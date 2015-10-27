# -*- coding:utf-8 -*-
# for kaikaidai
__author__ = 'wangtao'
import os
import pymssql
import sys
import re
from pymongo import MongoClient
from selenium import webdriver
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")

qSearch = re.compile(r"[1-9]\d*$")
qTime = re.compile(r"")

class kaikaidai_spider:

    def __init__(self):
        self.conn = None
        self.dbhost = "localhost"
        self.dbname = "crawler_db"
        self.dbusername = "sa"
        self.dbpasswd = "Mime123"
        self.dictkeyidx = {"nameidx": 0, "cardididx": 1, "telidx": 2, "phoneid": 3, "timeid":4}
        self.dictkey = ["name", "cardid", "telephone", "phonenum", "updatetime"]
        try:
            self.conn = pymssql.connect(host=self.dbhost, database=self.dbname,user=self.dbusername,password=self.dbpasswd,charset="utf8")
        except:
            # handle the exception
            return None
        else:
            pass

    def __del__(self):
        self.conn.close()

    def save_mssql_tupel(self,datatuple):
        self.save_mssql(datatuple[self.dictkey[0]],datatuple[self.dictkey[1]],datatuple[self.dictkey[2]],datatuple[self.dictkey[3]],datatuple[self.dictkey[4]])

    def save_mssql(self, name, cardid, telphone,phonenum, updatetime,dbname = "wdwy"):
        """
        save one tuple into mssql server
        :param name:
        :param cardid:
        :param phonenum:
        :param updatetime:
        :return:
        """
        str = "insert into %s(name,cardid,phoneno,sdate) values('%s', '%s', '%s', '%s')" % (dbname, name, cardid, phonenum, updatetime)
        print str
        cursor = self.conn.cursor()
        cursor.execute(str)
        self.conn.commit()
        cursor.close()


    def test_save_mssql(self):
        self.save_mssql("testname","testcardid","testphone","testsdate")

    def get_data_from_doc(self,itemnode):
        """

        :param itemnode: 待抽取结点
        :return: 数据tuple
        """
        retdict = dict()
        retdict[self.dictkey[0]] = itemnode.find_element_by_xpath("./tbody[1]/tr[1]/td[3]").text  # name
        retdict[self.dictkey[1]] = itemnode.find_element_by_xpath("./tbody[1]/tr[2]/td[2]").text  # cardid
        retdict[self.dictkey[2]] = itemnode.find_element_by_xpath("./tbody[1]/tr[2]/td[4]").text  # telephoneno
        retdict[self.dictkey[3]] = itemnode.find_element_by_xpath("./tbody[1]/tr[3]/td[4]").text  # phonenum
        retdict[self.dictkey[4]] = "unsupported"  # updatetime
        return retdict

    def get_kaikaidai(self):
        """
        get data from   http://www.kaikaidai.com/Lend/Black.aspx
        :return:
        """
        url = "http://www.kaikaidai.com/Lend/Black.aspx"
        driver = webdriver.PhantomJS()
        driver.get(url)
        while True:
            try:
                # extract data from curpage
                for elem in driver.find_elements_by_class_name("hmd_ytab"):
                    self.save_mssql_tupel(self.get_data_from_doc(elem))
            except:
                print "excetp happended!"
                driver.find_element_by_link_text("下一页").click()
            else:
                driver.find_element_by_link_text("下一页").click()

        driver.quit()


if __name__ == "__main__":
    wdwySpider = kaikaidai_spider()
    wdwySpider.get_kaikaidai()



