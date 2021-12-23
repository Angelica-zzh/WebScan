'''
Author: 21181214207
Date: 2021-12-22 06:18:28
LastEditors: 21181214207
LastEditTime: 2021-12-22 22:52:37
FilePath: /Documents/WebScan/webscan.py
'''
import re
from sqlite3.dbapi2 import connect
import sys
import time
import requests
from bs4 import BeautifulSoup
# from Match.Webfinger.webfinger import usage
from lib.config_ import *

class CmsScanner(object):
    def __init__(self,target) -> None:
        super().__init__()
        self.target = target
        self.start  = time.time()
        setting()

    #获取web信息
    def get_info(self):
        try:
            r = requests.get(url=self.target,headers=agent,timeout=3,verify=False)
            content = r.text
            try:
                title = BeautifulSoup(content,'lxml').title.text.strip()
                return str(r.headers),content,title.strip('\n')
            except:
                return str(r.headers),content,''
        except Exception as e:
            pass

    #指纹识别
    def check_rule(self,key,header,body,title):
        try:
            if 'title="' in key:
                if re.findall(rtitle,key)[0].lower() in title.lower():
                    return True
            elif 'body="' in key:
                if re.findall(rbody,key)[0] in body:return True
            else:
                if re.findall(rheader ,key)[0] in header:return True
        except Exception as e:
            pass

    #将数据库中的key拿出来进行匹配
    def handle(self, _id, header, body, title):
        name, key = check(_id)
        #满足一个条件即可的情况
        if '||' in key and '&&' not in key and '(' not in key:
            for rule in key.split('||'):
                if self.check_rule(rule, header, body, title):
                    print('%s[+] %s   %s%s' %(G, self.target, name, W))

                    break
        #只有一个条件的情况
        elif '||' not in key and '&&' not in key and '(' not in key:
            if self.check_rule(key, header, body, title):
                print('%s[+] %s   %s%s' %(G, self.target, name, W))
        #需要同时满足条件的情况
        elif '&&' in key and '||' not in key and '(' not in key:
            num = 0
            for rule in key.split('&&'):
                if self.check_rule(rule, header, body, title):
                    num += 1
            if num == len(key.split('&&')):
                print('%s[+] %s   %s%s' %(G, self.target, name, W))
        else:
            #与条件下存在并条件: 1||2||(3&&4)
            if '&&' in re.findall(rbracket, key)[0]:
                for rule in key.split('||'):
                    if '&&' in rule:
                        num = 0
                        for _rule in rule.split('&&'):
                            if self.check_rule(_rule, header, body, title):
                                num += 1
                        if num == len(rule.split('&&')):
                            print('%s[+] %s   %s%s' %(G, self.target, name, W))
                            break
                    else:
                        if self.check_rule(rule, header, body, title):
                            print('%s[+] %s   %s%s' %(G, self.target, name, W))
                            break
            else:
                #并条件下存在与条件： 1&&2&&(3||4)
                for rule in key.split('&&'):
                    num = 0
                    if '||' in rule:
                        for _rule in rule.split('||'):
                            if self.check_rule(_rule, title, body, header):
                                num += 1
                                break
                    else:
                        if self.check_rule(rule, title, body, header):
                            num += 1
                if num == len(key.split('&&')):
                    print('%s[+] %s   %s%s' %(G, self.target, name, W))

    def run(self):
        try:
            header,body,title = self.get_info()
            for _id in range(1,int(count())):
                try:
                    self.handle(_id,header,body,title)
                except Exception as e:
                    pass
        except Exception as e:
            print(e)
        finally:
            print('-'*54)
            print(u'%s[+] 指纹识别完成, 耗时 %s 秒.%s' %(O, time.time()-self.start, W))

def usage():
    print('usage: python %s http://www.qq.com' %sys.argv[0])
    sys.exit(0)

def main():
    banner()
    if len(sys.argv) != 2:
        usage()
    elif 'http' not in sys.argv[1]:
        usage()
    else:
        cms = CmsScanner(sys.argv[1])
        cms.run()

if __name__ == '__main__':
    main()