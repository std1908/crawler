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
# reload(sys)
# sys.setdefaultencoding('utf-8')

GDriveJSON = 'crawler-test-586486e61375.json'
GSpreadSheet = 'Article traffic'

class T17():

    def __init__(self):
        pass

    def Getdata(self,sheet):
        headers = { "Host": "t17.techbang.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-TW",
                    "Accept-Encoding": "gzip, deflate, br",
                    "DNT": "1",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1"}

        try:
            title_list = []
            traffic_list = []
            page = 1
            
            while True:
                # get article_list
                r = requests.get("https://t17.techbang.com/users/enterbox?page=" + str(page),headers=headers)
                soup = BeautifulSoup(r.text,'html.parser')

                all_article = soup.select("h4")
                if(all_article == []):
                    break
                for article in all_article:
                    title = article.text
                    href = (article.select('a')[0]['href'])
                    title_list.insert(0,title)
                    r = requests.get("https://t17.techbang.com"+href,headers=headers)
                    soup = BeautifulSoup(r.text,'html.parser')
                    for t in soup.select('.float-share.visible-desktop'):
                        traffic = t.text.split('閱')[0][1:]
                        if('千' in traffic):
                            traffic = traffic.replace('千','')
                            traffic = float(traffic) * 1000
                        elif('萬' in traffic):
                            traffic = traffic.replace('萬','')
                            traffic = float(traffic) * 10000
                        traffic_list.insert(0,int(traffic)) 
                page = page + 1

            worksheet().updatecell(sheet,title_list,traffic_list)

        except Exception as ex:
            traceback.print_exc()
            print(ex)