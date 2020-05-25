# -*- coding: UTF-8 -*-

from xfastest import xfastest
from enterbox import enterbox
from mobile01 import mobile01
from T17 import T17
from ck101 import ck101
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

GDriveJSON = 'crawler-b7cde5d7bc9e.json'
GSpreadSheetURL = "發文列表"
GSpreadSheet = 'Article traffic'

while True:
    try:
        scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key) 
        sh = gc.open(GSpreadSheet)

        worksheetCk = sh.worksheet("ck101")
        ck101().LoginAndGetdata(worksheetCk)
        time.sleep(60)
        gc.login()
        worksheetXf = sh.worksheet("xfastest")
        xfastest().LoginAndGetdata(worksheetXf)
        time.sleep(60)
        gc.login()
        worksheetMo = sh.worksheet("mobile01")
        mobile01().Getdata(worksheetMo)
        time.sleep(60)
        gc.login()
        worksheet17 = sh.worksheet("T17")
        T17().Getdata(worksheet17)
        time.sleep(60)
        gc.login()
        worksheetEn = sh.worksheet("Enterbox")
        enterbox().Getdata(worksheetEn)
        
        time.sleep(60)
    except Exception as ex:
        print('無法連線Google試算表', ex)
        traceback.print_exc()
        sys.exit(1)