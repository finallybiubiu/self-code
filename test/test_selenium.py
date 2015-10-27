# -*- coding:utf-8 -*-
from selenium import webdriver
import urllib
import urllib2

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

page = urllib2.urlopen("http://localhost/test_js.html").read()
print page


driver = webdriver.PhantomJS()
"""
driver.get('http://www.ip.cn/125.95.26.82')
print driver.find_element_by_id("result").text.split("/n")[0].split(u'来自：')[1]
"""
driver.get("http://localhost/test_js.html")
print driver.find_element_by_css_selector("p").text
print driver.find_element_by_css_selector("img").get_attribute("src")
#print driver.page_source


driver1 = webdriver.PhantomJS(desired_capabilities={'phantomjs.page.settings.resourceTimeout': '5000'})
driver1.get("http://www.pyworm.com/jsimg/")

try:
    print driver1.find_element_by_css_selector("img").get_attribute("src")
except:
    print driver1.page_source
else:
    pass


driver.quit()
