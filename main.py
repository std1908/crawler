# -*- coding: UTF-8 -*-

from mobile01 import mobile01
from T17 import T17
from Zentalk import Zentalk
from bs4 import BeautifulSoup
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

while True:
    try:
        scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        sh = gc.open(GSpreadSheet)
        worksheetMo = sh.worksheet("mobile01")
        mobile01().LoginAndGetdata(worksheetMo)
        time.sleep(100)
        worksheet17 = sh.worksheet("T17")
        T17().Getdata(worksheet17)
        time.sleep(100)
        worksheetZe = sh.worksheet("Zentalk")
        Zentalk().LoginAndGetdata(worksheetZe)

        time.sleep(144600)
    except Exception as ex:
        print('無法連線Google試算表', ex)
        traceback.print_exc()
        sys.exit(1)