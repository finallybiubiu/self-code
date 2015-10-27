# -*- coding:utf-8 -*-
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


class jiedai_spider:
    def __init__(self):
        self.dbhost = "localhost"
        self.dbname = "crawler_db"
        self.dbusername = "sa"
        self.dbpasswd = "Mime123"
        self.conn = None

        try:
            self.conn = pymssql.connect(host=self.dbhost, database=self.dbname,user=self.dbusername,password=self.dbpasswd,charset="utf8")
        except:
            # handle the exception
            return None
        else:
            pass

    def __del__(self):
        self.conn.close()

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
        print db_tuple
        self.db_colhdl.insert(db_tuple)

    def save_mssql(self, name, cardid, phonenum, updatetime,dbname = "wdwy"):
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


    def get_jiedai(self):
        """
        get data from   www.wangdaiwuyou.com
        :return:

        doc-tree:
        <div class="black_item">
            <div class="black_item_l">
                <div style="margin:40px 0 0px 35px;color:#ccc;">暂无照片</div>
            </div>
            <div class="black_item_r" style="width:350px;">
                <div style="border-top:0px;">姓名：邬伟敏</div>
                <div>手机：18616595597</div>
                <div>身份：310110198411021592</div>
                <div>地址：上海市杨浦区长阳路2087弄17号603室</div>
            </div>
            <div class="black_item_r" style="width:450px;">
                <div style="border-top:0px;">申报情况：你我贷 @ 2012-12-28</div>
                <div>欠款情况：￥81016.00元，拖欠：419天</div>
                <div>还款状态：未还</div>
                <div>提交备注：邬伟敏逾期未还项目</div>
            </div>
            <div style="clear:both;"></div>
        </div>
        """

        # 1 url
        url = "http://www.jiedai.cn/blacklist/"
        div_name = "black_item"
        driver = webdriver.PhantomJS()
        driver.get(url)
        # get the page number  depend the page one
        linklist = driver.find_element_by_id("page").find_elements_by_css_selector("a")[-2].text.decode("utf-8")
        page_nums = int(linklist)
        print "Total Page:", page_nums

        for page_num in range(1, page_nums):
            # get data from current page
            for pnode in driver.find_elements_by_class_name(div_name):
                try:
                    pname = pnode.find_element_by_xpath("./div[2]/div[1]").text.decode("utf-8").split("：")[1]  # 姓名
                    pCardid = pnode.find_element_by_xpath("./div[2]/div[3]").text.decode("utf-8").split("：")[1]  # 证件号
                    phonenum = pnode.find_element_by_xpath("./div[2]/div[2]").text.decode("utf-8").split("：")[1]  # 联系电话
                    updatetime = "unsupported"  # 更新时间

                    # filter the empty info
                    if pname != "":
                        self.save_mssql(pname, pCardid, phonenum, updatetime)
                except:
                    print sys.exc_info()[0],sys.exc_info()[1]
                else:
                    pass
            # reassign driver
            newurl = "%s/%d.html" % (url, page_num + 1)
            driver.get(newurl)
            print newurl
        driver.quit()

if __name__ == "__main__":
    wdwySpider = jiedai_spider()
    wdwySpider.get_wdblack()

