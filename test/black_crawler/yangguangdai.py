# -*- coding:utf-8 -*-
__author__ = 'wangtao'
import os
import pymssql
import sys
import re
from pymongo import MongoClient
from selenium import webdriver
from bs4 import BeautifulSoup
import chardet
reload(sys)
sys.setdefaultencoding("utf-8")

qSearch = re.compile(r"[1-9]\d*$")
qTime = re.compile(r"")


class yangguangdai_spider:
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

    def save_mssql(self, name, cardid, phonenum, updatetime, dbname="wdwy"):
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

    def get_total_pagesnum(self, driver):
        """
        get the total page number
        :param driver: webdriver variable after reading the html
        :return: page_nums --total Page numbers
        """
        page_nums = 1
        try:
            linkurl = driver.find_element_by_link_text(u"下一页").get_attribute("href")
        except:
            page_nums = 1
        else:
            print linkurl
            page_nums = linkurl.split("/")[-1].split(".")[0]
            print page_nums
        return page_nums


    def get_wdblack(self):
        """
        get data from   www.wangdaiwuyou.com
        :return:

        doc-tree:
        <ul class="f12 pt10 pb10 border-dash-b">
            <li class="w297 pl10 fl tall lh30">
                <div class="lh22"><span class="dinb w60 talr col-9">账户：</span><a target="_blank" title="黄泽林_44030619871128113X_欠钱不还_老赖_贷款跑路_骗子_黑名单" style="color:#333333" href="/s/Heimingdan/id/1473.html">laidaopeng</a></div>
                <div class="lh22"><span class="dinb w60 talr col-9">姓名：</span><a target="_blank" title="黄泽林_44030619871128113X_欠钱不还_老赖_贷款跑路_骗子_黑名单" style="color:red;" class="b" href="/s/Heimingdan/id/1473.html">黄泽林</a></div>
                <div class="lh22"><span class="dinb w60 talr col-9">身份证：</span><b class="red">44030619871128113X</b></div>
                <div class="lh22"><span class="dinb w60 talr col-9">邮箱：</span>laidaopeng@126.com</b></div>
                <div class="lh22"><span class="dinb w60 talr col-9">手机号：</span></div>
                <div class="lh22"><span class="dinb w60 talr col-9">家庭住址：</span></div>
                <div class="lh22"><span class="dinb w60 talr col-9">家庭电话：</span></div>
            </li>
            <li class="w300 fl tall lh30">
                <div class="lh22"><span class="col-9 dinb w60 talr">工作单位：</span></div>
                <div class="lh22"><span class="col-9 dinb w60 talr">单位地址：</span></div>
                <div class="lh22"><span class="col-9 dinb w60 talr">职位：</span></div>
            </li>
            <li class="w380 pl3 fl lh30 pr">
                <a class="pa" style="bottom:8px; right:2px;" target="_blank" title="黄泽林_44030619871128113X_欠钱不还_老赖_贷款跑路_骗子_黑名单" href="/s/Heimingdan/id/1473.html">详细信息 »</a>
                <div class="lh22"><span class="col-9 dinb w90 talr">逾期总金额：</span>906.35</div>
                <div class="lh22"><span class="col-9 dinb w90 talr">逾期借款笔数：</span>2</div>
                <div class="lh22"><span class="col-9 dinb w90 talr">最大逾期天数：</span>1050</div>
            </li>
            <li class="clrbo"></li>
        </ul>

        """

        # 1 url
        rooturl = "http://ygjiedai.com.cn/s/blacklist"
        url = "http://ygjiedai.com.cn/s/blacklist.html"
        div_name = "f12 pt10 pb10 border-dash-b"
        driver = webdriver.PhantomJS()
        driver.get(url)
        # get the page number  depend the page one
        page_nums = self.get_total_pagesnum(driver)
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
            newurl = "%s/page/%d.html" % (rooturl, page_num + 1)
            driver.get(newurl)
            print newurl

        driver.quit()

if __name__ == "__main__":
    wdwySpider = yangguangdai_spider()
    wdwySpider.get_wdblack()

