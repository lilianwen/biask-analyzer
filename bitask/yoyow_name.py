#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import io
import sys
import re
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote
import string
import operator;
import xlwt

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


#获取当前脚本文件所在的路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

#通过url获取网页
def getHtml(url):
    # 要设置请求头，让服务器知道不是机器人
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
    headers = {'User-Agent': user_agent}

    re=urllib.request.Request(url,headers=headers);
    page = urllib.request.urlopen(re);
    html = page.read()
    return html.decode("UTF-8")
    
def getYOYOW(user_name):
    url = "https://www.bitask.org/people/"+user_name
    print(url)
    url=quote(url,safe=string.printable)#解决url中含有中文的问题
    user_page=str(getHtml(url))
    #print(user_page)
    yoyow_pos=user_page.find(">yoyow账号：")
    if yoyow_pos == -1:
        return "0"
    print(yoyow_pos)
    print(user_page[yoyow_pos+9:yoyow_pos+21])
    yoyow_str=user_page[yoyow_pos+9:yoyow_pos+17]
    print(yoyow_str)
    
    return yoyow_str
    
#print(getVA("风青萍"))

def GetPeople():
    list_of_url=[]
    user_names=[]
    #list_of_url.append("https://www.bitask.org/people/")
    for i in range(41,61):
        url = "https://www.bitask.org/people/page-%d" %i
        list_of_url.append(url)
    for one_url in list_of_url:
        people_page=str(getHtml(one_url))
        print(len(people_page))
        #print(people_page)
        user_name_pos=0
        for i in range(0,20):
            user_name_pos = people_page.find("aw-user-name", user_name_pos)
            user_name=people_page[user_name_pos+14:user_name_pos+50]
            user_name=user_name.split("<")[0]
            user_names.append(user_name)
            #print(user_name)
            #print(user_name_pos)
            user_name_pos +=1
    return user_names
            
            
#print(getVA("lilianwen"))
       
user_names=GetPeople()
name_yyw=[]
for one in user_names:
    one_name_yoyow=[]
    yyw = getYOYOW(one)
    if yyw == "0":
        continue
    one_name_yoyow.append(one)
    one_name_yoyow.append(yyw)
    name_yyw.append(one_name_yoyow)

print(name_yyw)


with open("account_map.txt","w",encoding='utf-8') as cf:
    for one in name_yyw:
        record=str(one[0])+" "+str(one[1])+"\n"
        cf.write(record)
      


