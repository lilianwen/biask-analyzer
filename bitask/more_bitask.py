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
    
def getVA(user_name):
    url = "https://www.bitask.org/people/"+user_name
    print(url)
    url=quote(url,safe=string.printable)#解决url中含有中文的问题
    user_page=str(getHtml(url))
    #print(user_page)
    agree_pos=user_page.find("icon-agree")
    #print(agree_pos)
    #print(user_page[agree_pos+55:agree_pos+70])
    agree_str=user_page[agree_pos+55:agree_pos+70]
    #print(agree_str.split("<")[0])
    agree_num=int(agree_str.split("<")[0])
    print(agree_num)
    
    #收益
    agree_energy_pos=user_page.find("点赞能量")
    reward_pos=user_page.find("收益", agree_energy_pos+1)
    print("收益：")
    print(reward_pos)
    reward_str=user_page[reward_pos+38:reward_pos+70]
    #print(reward_str)
    print(user_page[reward_pos:reward_pos+70])
    reward_num=float(reward_str.split("&nbsp")[0])
    print(reward_num)
    
    
    answer_pos=user_page.find("page_answer")
    answer_str=user_page[answer_pos+54:answer_pos+90]
    print(user_page[answer_pos+54:answer_pos+90])
    print(answer_str.split("<")[0])
    answer_num=int(answer_str.split("<")[0])
    print(answer_num)
    
    VA=float(agree_num)/answer_num
    #print(VA)
    
    return agree_num,answer_num,VA,reward_num
    
#print(getVA("风青萍"))

def GetPeople():
    list_of_url=[]
    user_names=[]
    list_of_url.append("https://www.bitask.org/people/")
    for i in range(2,6):
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
name_va=[]
for one in user_names:
    one_name_va=[]
    agree_n,answer_n,va,reward = getVA(one)
    if answer_n < 100:#过滤掉回答问题数少于100的
        continue
    one_name_va.append(one)
    one_name_va.append(agree_n)
    one_name_va.append(answer_n)
    one_name_va.append(va)
    one_name_va.append(reward)
    name_va.append(one_name_va)

name_va.sort(key=lambda x:x[4], reverse=True)#lambda x:x[3]返回list的第四个数据
print(name_va)


work_book = xlwt.Workbook() #创建工作簿
sheet1 = work_book.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建shee
sheet1.write(0,0,"昵称")
sheet1.write(0,1,"点赞数")
sheet1.write(0,2,"回答问题数")
sheet1.write(0,3,"V/A值")
sheet1.write(0,4,"收益（yoyow）")
i=1
for one in name_va:
    #print("[%d][%s][点赞数=%d][回答问题数=%d][%f][收益：%f yoyow]" %(i, one[0], one[1], one[2], one[3], one[4]))
    
    print("[%d][%s][收益：%f yoyow]" %(i, one[0], one[4]))
    sheet1.write(i,0,one[0])
    sheet1.write(i,1,one[1])
    sheet1.write(i,2,one[2])
    sheet1.write(i,3,one[3])
    sheet1.write(i,4,one[4])
    i +=1
work_book.save('bitask_va.xls')#保存文件       


