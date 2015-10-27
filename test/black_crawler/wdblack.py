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
# 网贷黑名单

qSearch = re.compile(r"[1-9]\d*$")
qTime = re.compile(r"")

class wdblack_spider:
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

    def get_wdblack(self):
        """
        from http://p2pzxw.com/index.asp
        :return:
        crawl data
        doc tree:
        <div class="yqsj_kk">
	        <div style="width:150px; float:left; padding:10px 0px; line-height:25px;">
                <div style="width:130px; float:left;"><img src="images/yqsj_tx.jpg" width="100" alt="网贷,网络借贷" /></div>
                <div style="width:130px; float:left; margin-top:5px;">来源：人人贷</div>
            </div>
			<div style="width:250px; float:left; text-align:left; line-height:25px; padding:10px 0px 0px 5px;">
                <div style="width:250px; float:left;">姓名：<font style="color:#8f253c;">周小红</font></div>
                <div style="width:250px; float:left;">证件号：<font style="color:#8f253c;"></font></div>
                <div style="width:250px; float:left;">性别：女</div>
                <div style="width:250px; float:left;">身份证地址：</div>
                <div style="width:250px; float:left;">家庭地址：</div>
                <div style="width:250px; float:left;">联系电话：</div>
            </div>
			<div style="width:230px; float:left; text-align:left; line-height:25px; padding:10px 0px 0px 5px;">
                <div style="width:230px; float:left;">欠款本息总额：￥<font style="color:#8f253c;">15000</font></div>
                <div style="width:230px; float:left;">逾期总罚息：1000</div>
                <div style="width:230px; float:left;">逾期笔数：6笔</div>
                <div style="width:230px; float:left;">网站代还笔数：6笔</div>
                <div style="width:230px; float:left;">最长逾期天数：35天</div>
                <div style="width:230px; float:left;">更新时间：2015-8-3</div>
            </div>
	   </div>

        """

        # 1 url
        url = "http://p2pzxw.com/index.asp?Page=1"
        div_name = "yqsj_kk"
        driver = webdriver.PhantomJS()
        driver.get(url)
        pagecode_type = "gb2312"
        # get the page number  depend the page one
        linklist = driver.find_element_by_link_text("尾页").get_attribute("href")
        pagenums = re.search(r"[0-9]\d*$", linklist).group(0)
        pagenums = int(str(pagenums))
        page_nums = int(pagenums)
        print "Total Page:", page_nums

        for page_num in range(1, page_nums):
            # get data from current page
            for pnode in driver.find_elements_by_class_name(div_name):
                try:
                    pname = pnode.find_element_by_xpath("./div[2]/div[1]").text.decode("utf-8").split("：")[1]  # 姓名
                    pCardid = pnode.find_element_by_xpath("./div[2]/div[2]").text.decode("utf-8").split("：")[1]  # 证件号
                    phonenum = pnode.find_element_by_xpath("./div[2]/div[6]").text.decode("utf-8").split("：")[1]  # 联系电话
                    updatetime = pnode.find_element_by_xpath("./div[3]/div[6]").text.decode("utf-8").split("：")[1]  # 更新时间
                    # filter the empty info
                    if pname != "":
                        self.save_mssql(pname, pCardid, phonenum, updatetime, "wdhmd")
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
    wdwySpider = wdblack_spider()
    wdwySpider.get_wdblack()

