# -*- coding:utf-8 -*-
__author__ = 'wangtao'
import os
import sys
from selenium import webdriver



class icb_excption_interpreter:
    """
    翻译经营异常企业信息---总局
    """
    def __init__(self,url):
        self.url = url
        self.driver = webdriver.PhantomJS()
        self.driver.get(self.url)
        self.contdiv = self.driver.find_element_by_class_name("cont-r-b")

    def __del__(self):
        if self.driver is not None:
            self.driver.quit()


    def get_registinfo(self):
        """
            1.注册号
            2.名称
            3.类型
            4.法定代表人
            5.注册资本
            6.成立日期
            7.营业期限自
            8.营业期限至
            9.登记机关
            10.经营状态
            10. SOURCE：1001
            11.TIME:GETDATE()
        获取以上字段的信息
        :return:
        """

        contdiv = self.contdiv.find_element_by_xpath("./div[4]/table[1]")
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
        # 1 注册号

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
    expurl = "http://gsxt.saic.gov.cn/zjgs/notice/view?uuid=ckWqpmOpcWOa99QnhSeyx00RIwy.ljusX.2gYb9CKzg=&tab=01"
    zjspider = icb_excption_interpreter(expurl)
    zjspider.get_registinfo()







