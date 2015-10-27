# -*- coding:utf-8 -*-
__author__ = 'wangtao'
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

url = r"http://gsxt.lngs.gov.cn/saicpub/entPublicitySC/entPublicityDC/entPublicity/search/searchmain.jsp"
page_html = urllib2.urlopen(url).read()
secucodedir = r"E:\verifyims\downsecurecode\\"



def get_authcode(cookie_para=None):
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
        cookiestr = COOKIESTR +  JESSIONSTR + CNDATASTR
        opener.addheaders.append(('Cookie', cookiestr))
    except:
        raise
    else:
        urllib2.install_opener(opener)

    imgfile = urllib2.urlopen(url).read()
    #  save securecode
    imgname = "verficode.jpeg"
    if os.path.isdir(secucodedir):
        imgname = secucodedir + imgname
    imgfp = open(imgname, "wb+")
    imgfp.write(imgfile)
    imgfp.close()
    # get securecode value
    authcode = str(pytesseract.image_to_string(Image.open(imgname), lang='chi_sim'))
    return authcode



driver = webdriver.Firefox()
driver.set_page_load_timeout(20)
#driver = webdriver.PhantomJS()
#driver = webdriver.Firefox()
url = r"http://gsxt.lngs.gov.cn/saicpub/entPublicitySC/entPublicityDC/lngsSearchFpc.action"
keywords = "东软集团股份有限公司"

# 1获取网站的cookie
homeurl = r"http://gsxt.lngs.gov.cn/saicpub/"
search_home_url = r"http://gsxt.lngs.gov.cn/saicpub/entPublicitySC/entPublicityDC/entPublicity/search/searchmain.jsp"
driver.get(homeurl)
driver.get(search_home_url)
cookies_para = driver.get_cookies()
#设置搜索关键词
driver.execute_script(r"document.getElementById('solrCondition').value='东软集团股份有限公司';")
driver.execute_script("zdm();")
# getsecucode
authcode = get_authcode(cookies_para)
print authcode


# 设置form
driver.execute_script(r"document.getElementById('authCode').value=" + authcode + ";")
print driver.find_element_by_id("solrCondition").get_attribute("value")
driver.execute_script(r"document.getElementById('searchForm').action='" + url + "';")
driver.execute_script(r"document.getElementById('searchForm').submit();")

try:

    divelem = driver.find_element_by_id("listContent")
    elm = divelem.find_element_by_xpath("./div[1]/ul[1]/li[1]/a[1]")
except:
    print "we can't find"
else:
    print "we can find"
    elm.click()
    # 切换到新窗口里
    for hdl in driver.window_handles:
        if hdl == driver.current_window_handle:
            continue
        else:
            driver.switch_to.window(hdl)
            # 等待页面加载完成
            WebDriverWait(driver,60).until(lambda brow: brow.find_element_by_id("s_gs_dj_1").find_element_by_id("jibenxinxi"))
    print driver.find_element_by_id("s_gs_dj_1").get_attribute("innerHTML")

# driver.quit()

