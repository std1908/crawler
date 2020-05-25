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
reload(sys)
sys.setdefaultencoding(utf-8)

class mobile01():

    def __init__(self):
        pass

    def Getdata(self,sheet):
        headers = { "Host": "www.mobile01.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-TW",
                    "Accept-Encoding": "gzip, deflate",
                    "DNT": "1",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1"}


        try:
            title_list = []
            traffic_list = []
            page = 1

            while True:
                # get article_list
                r = requests.get("https://www.mobile01.com/userinfo.php?id=3310841&p=" + str(page),headers=headers)
                soup = BeautifulSoup(r.text,'html.parser')

                all_article = soup.find_all(class_='l-searchCard__content')
                if(all_article == []):
                    break
                for article in all_article:
                    title = article.select('a')[0].text.strip()
                    title_list.insert(0,title)
                    traffic = article.find_all(class_='o-fNotes o-fSubMini')[1].text
                    traffic_list.insert(0,int(traffic)) 
                page = page + 1

            worksheet().updatecell(sheet,title_list,traffic_list)


        except Exception as ex:
            traceback.print_exc()
            print(ex)