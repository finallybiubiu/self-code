# -*- coding:utf-8 -*-
__author__ = 'wangtao'
import os
import sys
import re
from selenium import webdriver
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding("utf-8")

qSearch = re.compile(r"[1-9]\d*$")

def test():
    url = "http://www.wangdaiwuyou.com/wdda.asp?Page=107"
    rel_grp = qSearch.search(url).group()
    print rel_grp

    url = "http://localhost/xpath_test.html"
    div_class_name = "yqsj_k"
    driver = webdriver.PhantomJS()
    driver.get(url)

    linkstr = driver.find_element_by_link_text(u"尾页").get_attribute("href")
    print linkstr
    driver.quit()


"""

for divnode in driver.find_elements_by_class_name(div_class_name):
    print "############################################################"
    print divnode.find_element_by_xpath("./div[2]/div[1]/font[1]").text.decode("utf-8")
    print divnode.find_element_by_xpath("./div[2]/div[2]/font[1]").text.decode("utf-8")

"""

def test_page_encoding():
    url = "http://localhost/xpath_test_encoding.html"
    driver = webdriver.PhantomJS()
    driver.get(url)

    node = driver.find_element_by_class_name("wdzs_sz").find_elements_by_css_selector("a")
    strurl = node[3].get_attribute("href")
    print strurl
    driver.quit()


def func(para1,para2):
    """
    func just for test
    :param para1:param 1 comment
    :param para2:param  2 comment
    :return: nothing
    """
    while True:  # condition
        if para1 == para2:
            print para1, para2    # print
            break
        elif para1 > para2:
            print "elif"
            continue
        else:
            pass


def func2(para2,para3):
    """

    :param para2:
    :param para3:
    :return:
    """
    return None












if __name__ == "__main__":
    #test_page_encoding()
    listvar = [1,3,4,5,"hggyguuy"]
    print len(listvar)

    str = "更新时间："
    print str.split("：")[1]