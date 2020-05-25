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
reload(sys)
sys.setdefaultencoding('utf-8')

class ck101():

    def __init__(self):
        pass

    def LoginAndGetdata(self,sheet):
        try:
            title_list = []
            traffic_list = []
            page = 1

            loginurl = "https://ck101.com/home.php?mod=space&uid=6356745&do=thread&view=me&from=space"
            username = 'enterbox.tw@gmail.com'
            password = 'b74AS@hnZvXhJHs'

            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            driver = webdriver.Firefox(firefox_options=options)
            driver.get(loginurl)
            time.sleep(0.5)

            driver.find_element_by_link_text('登入').click()
            time.sleep(2)
            driver.find_element_by_name('username').send_keys(username)
            time.sleep(0.5)
            driver.find_element_by_name('password').send_keys(password)
            time.sleep(0.5)
            driver.find_element_by_name('loginsubmit').click()
            time.sleep(0.5)

            while True:
                driver.get('https://ck101.com/home.php?mod=space&uid=6356745&do=thread&view=me&from=space&page=' + str(page))
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
                    traffic_list.insert(0,int(driver.find_elements_by_tag_name('em')[index].text))
                page = page + 1
            worksheet().updatecell(sheet,title_list,traffic_list)

        except Exception as ex:
            traceback.print_exc()
            print(ex)