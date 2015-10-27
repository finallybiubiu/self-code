# -*- coding:utf-8 -*-
from PIL import Image
import pytesseract
import sys
import time
import datetime
import os
import random
import hashlib
import urllib
import urllib2
import cookielib
from pyocr import pyocr
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class liaon_spider:
    def __init__(self, keywords):
        self.url = r"http://gsxt.lngs.gov.cn/saicpub/entPublicitySC/entPublicityDC/entPublicity/search/searchmain.jsp"
        self.secucodedir = r"E:\verifyims\downsecurecode\\"
        self.keywords = keywords
        self.search_home_url = r"http://gsxt.lngs.gov.cn/saicpub/entPublicitySC/entPublicityDC/entPublicity/search/searchmain.jsp"
        self.homeurl = r"http://gsxt.lngs.gov.cn/saicpub/"
        self.form_action_url = r"http://gsxt.lngs.gov.cn/saicpub/entPublicitySC/entPublicityDC/lngsSearchFpc.action"
        self.max_try_time_per_keywords = 5 #  验证码识别存在误差，每个关键字最多尝试5次

    def get_authcode(self, cookie_para=None):
        #get secucodename
        imgname = hashlib.md5(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).hexdigest() + ".jpeg"
        # for get the pure number securecode
        num = 3 * int(random.uniform(1,1000))
        url = "http://gsxt.lngs.gov.cn/saicpub/commonsSC/loginDC/securityCode.action?tdate=" + str(num)
        opener = ""
        try:
            opener = urllib2.build_opener()
            COOKIESTR = cookie_para[0]["name"] + "=" + cookie_para[0]["value"] + ";"
            JESSIONSTR = cookie_para[1]["name"] + "=" + cookie_para[1]["value"] + ";"
            CNDATASTR = cookie_para[2]["name"] + "=" + cookie_para[2]["value"] + ";"
            cookiestr = COOKIESTR + JESSIONSTR + CNDATASTR
            opener.addheaders.append(('Cookie', cookiestr))
        except:
            raise
        else:
            urllib2.install_opener(opener)
        imgfile = urllib2.urlopen(url).read()
        #  save securecode
        if os.path.isdir(self.secucodedir):
            imgname = self.secucodedir + imgname
        imgfp = open(imgname, "wb+")
        imgfp.write(imgfile)
        imgfp.close()
        # get securecode value
        authcode = str(pytesseract.image_to_string(Image.open(imgname), lang='chi_sim'))
        return authcode

    def test_selenium(self):
        keywords = self.keywords
        homeurl = self.homeurl
        search_home_url = self.search_home_url
        url = self.form_action_url
        try_time = 0

        driver = webdriver.Firefox()
        driver.set_page_load_timeout(20)
        driver.get(homeurl)
        driver.get(search_home_url)
        cookies_para = driver.get_cookies()
        # 设置搜索关键词
        driver.execute_script(r"document.getElementById('solrCondition').value='%s';" % keywords)
        driver.execute_script("zdm();")

        while try_time < self.max_try_time_per_keywords:
            try:
                # getsecucode
                authcode = self.get_authcode(cookies_para)
                print authcode
                # 设置form
                driver.execute_script(r"document.getElementById('authCode').value=" + authcode + ";")
                driver.execute_script(r"document.getElementById('searchForm').action='" + url + "';")
                driver.execute_script(r"document.getElementById('searchForm').submit();")
                divelem = driver.find_element_by_id("listContent")
                elm = divelem.find_element_by_xpath("./div[1]/ul[1]/li[1]/a[1]")
            except Exception:
                print "[%d]try again for %s" % (try_time, keywords)
                try_time += 1
                continue
            else:
                print "we can find"
                elm.click()
                # 切换到公司信息详情新窗口里
                for hdl in driver.window_handles:
                    if hdl == driver.current_window_handle:
                        continue
                    else:
                        driver.switch_to.window(hdl)
                        # 等待页面加载完成
                        WebDriverWait(driver,60).until(lambda brow: brow.find_element_by_id("s_gs_dj_1").find_element_by_id("jibenxinxi"))
                self.interpreter_baseinfo(driver)
                break
        # get info failed,just record the error
        if try_time == self.max_try_time_per_keywords:
            print "failed to get "
        driver.quit()

    def interpreter_baseinfo(self, driver):
        contdiv = driver.find_element_by_id("s_gs_dj_1").find_element_by_xpath("./div[1]/table[1]")
        # print contdiv.get_attribute("innerHTML")
        r_no = contdiv.find_element_by_xpath("./tbody[1]/tr[2]/td[1]").text
        r_name = contdiv.find_element_by_xpath("./tbody[1]/tr[2]/td[2]").text
        r_type = contdiv.find_element_by_xpath("./tbody[1]/tr[3]/td[1]").text
        r_legalperson = contdiv.find_element_by_xpath("./tbody[1]/tr[3]/td[2]").text
        r_capital = contdiv.find_element_by_xpath("./tbody[1]/tr[4]/td[1]").text
        r_estdate = contdiv.find_element_by_xpath("./tbody[1]/tr[4]/td[2]").text
        r_begintime = contdiv.find_element_by_xpath("./tbody[1]/tr[6]/td[1]").text
        r_endtime = contdiv.find_element_by_xpath("./tbody[1]/tr[6]/td[2]").text
        r_regorgan = contdiv.find_element_by_xpath("./tbody[1]/tr[8]/td[1]").text
        r_opstat = contdiv.find_element_by_xpath("./tbody[1]/tr[9]/td[1]").text

        print r_no
        print r_name
        print r_type
        print r_legalperson
        print r_capital
        print r_estdate
        print r_begintime
        print r_endtime
        print r_regorgan
        print r_opstat

if __name__ == "__main__":
    lnspider = liaon_spider("东软集团股份有限公司")
    lnspider.test_selenium()
