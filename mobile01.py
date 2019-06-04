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

class mobile01():

    def __init__(self):
        pass

    def LoginAndGetdata(self,sheet):
        loginheaders = {
                "Host": "www.mobile01.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-TW",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "TE": "Trailers" 
            }

        loginurl = "https://www.mobile01.com/login.php?link=%2F"

        logindata = {
                "login_email":"	enterbox.tw@gmail.com",
                "login_password":"xoswyk-Degpe5-hopsam"
        }

        loginResponseRes = requests.post(loginurl, data = logindata, headers = loginheaders)
        sessionID = loginResponseRes.cookies.get_dict()['PHPSESSID']


        headers = { "Host": "www.mobile01.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-TW",
                    "Accept-Encoding": "gzip, deflate, br",
                    "DNT": "1",
                    "Connection": "keep-alive",
                    "Cookie": "PHPSESSID=" + sessionID + "; googlesearchtype=%5Bobject%20Object%5D; googlesearchcate=0; googlesearchsubcates=0; googlesearchsubcate=0; userinfo[lastlogin]=1554436565; userinfo[currentlogin]=1554460315; userinfo[id]=3310841; userinfo[username]=EnterBox; userinfo[pass]=z384XoLFyp2vUrvtrzCSFwjfRL%2B8icMYXryiwqcsnjPTRRje%2F8mIp%2B%2BiOEHRDwDM; userinfo[timezone]=8.0; loginstat=1; tagmode=1; forumnavi=1",
                    "Upgrade-Insecure-Requests": "1",
                    "TE": "Trailers" }

        try:
            title_list = []
            traffic_list = []
            page = 1

            while True:
                # get article_list
                r = requests.get("https://www.mobile01.com/mytopics.php?c=0&f=0&v=all&sort=topictime&p=" + str(page),headers=headers)
                soup = BeautifulSoup(r.text,'html.parser')

                allpage = int(soup.select("p.numbers")[0].text[soup.select("p.numbers")[0].text.find('共')+1])
                if(page > allpage):
                    worksheet().updatecell(sheet,title_list,traffic_list)
                    break
                
                all_article = soup.select("tr")
                for article in all_article:
                    if(article.text.split('\n')[1] != '主題'):
                        title = article.text.split('\n')[1]
                        traffic = (article.select('.subject-text a ')[0]['title']).split(' ')[1]
                        title_list.insert(0,title)
                        traffic_list.insert(0,int(traffic))
                page = page +1

        except Exception as ex:
            traceback.print_exc()
            print(ex)