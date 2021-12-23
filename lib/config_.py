'''
Author: 21181214207
Date: 2021-12-22 06:18:57
LastEditors: 21181214207
LastEditTime: 2021-12-22 23:00:16
FilePath: /Documents/WebScan/lib/config_.py
'''
import re
import os
import sys
import importlib
import sqlite3
import urllib3

#colour
W = '\033[0m'
G = '\033[1;32m'
R = '\033[1;31m'
O = '\033[1;33m'
B = '\033[1;34m'

#User-Agent
agent = {'UserAgent':'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))'}

#re
rtitle = re.compile(r'title="(.*)"')
rheader  = re.compile(r'header="(.*)"')
rbody    = re.compile(r'body="(.*)"')
rbracket = re.compile(r'\((.*)\)')

path = os.path.dirname(os.path.abspath(__file__))   

#ssl错误
def setting():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#banner
def banner():
	banner = '''
              _                           
 __      _____| |__    ___  ___ __ _ _ __  
 \ \ /\ / / _ \ '_ \  / __|/ __/ _` | '_ \ 
  \ V  V /  __/ |_) | \__ \ (_| (_| | | | |
   \_/\_/ \___|_.__/  |___/\___\__,_|_| |_|
                                                                             
    '''
	print(B + banner + W)
	print('-'*54)


def check(_id):
    with sqlite3.connect(path+'/web.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT name,keys FROM `fofa` WHERE id=\'{}\''.format(_id))
        for row in result:
            return row[0],row[1]



def count():
	with sqlite3.connect(path + '/web.db') as conn:
		cursor = conn.cursor()
		result = cursor.execute('SELECT COUNT(id) FROM `fofa`')
		for row in result:
			return row[0]