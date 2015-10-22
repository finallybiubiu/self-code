# -*- coding:utf-8 -*-
__author__ = 'wangtao'
import os
import sys
from selenium import webdriver
import re
import time
class MadeReport:
    def __init__(self):
        self.repurl = r"http://99.48.58.207:8080/job/test/HTML_Report"
        self.phantompath = r"D:\apache-jmeter-2.13\bin\phantomjs.exe"
        self.strtime = time.strftime(("%Y-%m-%d"),time.localtime())
        self.relpath = r"testresult\%s\html" % (self.strtime)
        self.driver = webdriver.PhantomJS(self.phantompath)
        self.subdriver = webdriver.PhantomJS(self.phantompath)
        self.scur_path = os.getcwd()
        self.rooturl = r"%s\%s" % (self.scur_path,self.relpath)
        self.summaryname = r"%s\summary.html" % self.rooturl

        self.html_head_elm ="<head> \
<META http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\
<title>WebLoad Test Report:[login]</title>\
<style type=\"text/css\">\
				body {\
					font:normal 68% verdana,arial,helvetica;\
					color:#000000;\
				}\
				table tr td, table tr th {\
					font-size: 68%;\
				}\
				table.details tr th{\
				    color: #ffffff;\
					font-weight: bold;\
					text-align:center;\
					background:#2674a6;\
					white-space: nowrap;\
				}\
				table.details tr td{background:#eeeee0;white-space: nowrap;}\
				h1 {margin: 0px 0px 5px; font: 165% verdana,arial,helvetica}\
				h2 {margin-top: 1em; margin-bottom: 0.5em; font: bold 125% verdana,arial,helvetica}\
				h3 {margin-bottom: 0.5em; font: bold 115% verdana,arial,helvetica}\
				.Failure {font-weight:bold; color:red;}\
				.page_details{display: none;}\
.page_details_expanded{display: block;display: table-row;}\
</style>\
</head>\n"

    def write_htmlheader(self):
        fp = open(self.summaryname,"w+")
        fp.write("<html>\n")
        fp.write(self.html_head_elm)
        fp.write("<body>\n")
        fp.write("<h1>WebLoad Test Repost:[summary]</h1>\n")
        strtime = "<h2>Date report : %s</h2>\n" % (self.strtime)
        fp.write(strtime)
        fp.write("<hr size=\"1\">\n")
        fp.write("<table width=\"50%\" cellspacing=\"2\" cellpadding=\"5\" border=\"0\" class=\"details\" align=\"center\">\n")
        fp.write("<tr style=\"text-align:center\"><td>pagenum</td><td>result</td></tr>\n")
        fp.close()
        print "call write_htmlheader"

    def write_htmlfooter(self):
        fp = open(self.summaryname,"a+")
        fp.write("</table>\n")
        fp.write("</body>\n")
        fp.write("</html>\n")
        fp.close()
        print "call write_htmlfooter"

    def write_oneitem(self,url,failflg):
        fp = open(self.summaryname,"a+")
        strresult = ""
        # no fail records
        if failflg == 0:
            strresult = "SUCCESS"
        else:
            strresult = "FAIL"
        pagename = url.split(".")[0]
        str = "<tr><td><a href='%s/%s'>%s</a></td><td>%s</td>\n" % (self.repurl,url,pagename,strresult)
        fp.write(str)
        fp.close()
        print "call write_oneitem"

    def rep_collect(self):
        subdriver = self.subdriver
        #获取某目录下的文件的全路径，list
        rooturl = self.rooturl

        print rooturl
        for url in os.listdir(rooturl):
            if url == "summary.html":    # 过滤掉生成的文件
                continue
            paramurl = url
            url = "%s\%s" % (rooturl,url)
            subdriver.get(url)
            try:
                sfailnum = subdriver.find_elements_by_tag_name("table")[1].find_element_by_xpath("./tr[2]/td[2]").text
                failnum = int(sfailnum)
                self.write_oneitem(paramurl,failnum)
            except:
                self.write_oneitem(paramurl,-1)
            else:
                pass

    def __del__(self):
        if self.driver is not None:
            self.driver.quit()
        if self.subdriver is not None:
            self.subdriver.quit()

if __name__ == "__main__":
    mp = MadeReport()
    mp.write_htmlheader()
    mp.rep_collect()
    mp.write_htmlfooter()
