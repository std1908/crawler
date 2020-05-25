# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from worksheet import worksheet
import sys
import time
import datetime
import gspread
import traceback  
from oauth2client.service_account import ServiceAccountCredentials as SAC
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
import os
# reload(sys)
# sys.setdefaultencoding('utf-8')

class xfastest():

    def __init__(self):
        pass

    def LoginAndGetdata(self,sheet):
        try:
            title_list = []
            traffic_list = []
            page = 1

            loginurl = "https://www.xfastest.com/"
            username = 'enterbox'
            password = 'hr-38m4=2im'

            options = webdriver.FirefoxOptions()
            # options.add_argument("--headless")
            driver = webdriver.Firefox(firefox_options=options)
            driver.get(loginurl)
            time.sleep(0.5)

            driver.find_element_by_name('username').send_keys(username)
            time.sleep(0.5)
            driver.find_element_by_name('password').send_keys(password)
            time.sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div[2]/div[1]/div/div[2]/form/div/div/table/tbody/tr/td[5]/button').click()
            time.sleep(0.5)

            while True:
                driver.get('https://www.xfastest.com/home.php?mod=space&uid=274220&do=thread&view=me&from=space&page=' + str(page))
                time.sleep(0.5)
                if(driver.find_elements_by_class_name('emp')):
                    if(driver.find_elements_by_class_name('emp')[0].text == '還沒有相關的帖子'):
                        driver.close()
                        break
                for title in driver.find_elements_by_tag_name('th'):
                    if(title.text == '主題'):
                        continue
                    title_list.insert(0,title.text)
                for index in range(len(driver.find_elements_by_tag_name('em'))):
                    if(index %2 != 0):
                        continue
                    if(driver.find_elements_by_tag_name('em')[index].text != ''):
                        traffic_list.insert(0,int(driver.find_elements_by_tag_name('em')[index].text))
                page = page + 1
            worksheet().updatecell(sheet,title_list,traffic_list)

        except Exception as ex:
            traceback.print_exc()
            print(ex)