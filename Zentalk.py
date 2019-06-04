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
# reload(sys)
# sys.setdefaultencoding('utf-8')

class Zentalk():

    def __init__(self):
        pass

    def LoginAndGetdata(self,sheet):
        try:
            title_list = []
            traffic_list = []
            page = 1

            loginurl = "https://www.asus.com/tw/"
            username = 'enterbox.tw@gmail.com'
            password = 'qyxnag-2rusqe-taCtuj'

            options = webdriver.FirefoxOptions()
            # options.add_argument("--headless")
            driver = webdriver.Firefox(firefox_options=options)
            driver.get(loginurl)
            time.sleep(0.5)

            driver.find_element_by_class_name('postlink').click()
            time.sleep(0.5)
            driver.find_element_by_id('Front_txtAccountID').send_keys(username)
            time.sleep(0.5)
            driver.find_element_by_id('Front_txtPassword').send_keys(password)
            time.sleep(0.5)
            driver.find_element_by_id('btnLogin').click()
            time.sleep(0.5)

            while True:
                driver.get('https://www.asus.com/zentalk/tw/home.php?mod=space&uid=668806&do=thread&view=me&from=space&page=' + str(page))
                time.sleep(0.5)
                if(driver.find_elements_by_class_name('thread-title') == []):
                    driver.close()
                    break
                for title in driver.find_elements_by_class_name('thread-title'):
                    title_list.insert(0,title.text)
                for detail in driver.find_elements_by_class_name('us-thread-det'):
                    traffic = detail.text.split(' ')[1]
                    traffic_list.insert(0,int(traffic))
                page = page + 1
            worksheet().updatecell(sheet,title_list,traffic_list)

        except Exception as ex:
            traceback.print_exc()
            print(ex)