#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import re
import urllib.request;
import json
import socket
import random
import time




def getPage(url,timeout=5,referer=""):
    socket.setdefaulttimeout(timeout)
    # 要设置请求头，让服务器知道不是机器人
    # user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a MicroMessenger/5.2.1'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
    headers = {'User-Agent': user_agent}
    re=urllib.request.Request(url,headers=headers);
    print(referer)
    if referer != "":
        re.add_header("Referer", referer)
    try:
        page = urllib.request.urlopen(re);
    except urllib.error.HTTPError as e:
        return e.code,""
    else:
        return 200,page.read().decode("UTF-8")




def getQuestionTitle(page):
    page = str(page)
    question_title_pos=page.find("mod-head", 0)
    #print("question_title_pos=%d" %question_title_pos)
    if question_title_pos != -1:
        question_title=page[question_title_pos:question_title_pos+150]
        question_title_pos=page.find("<h1>",question_title_pos)
        question_title=page[question_title_pos+4:question_title_pos+150]
        question_title=question_title.replace("t","")
        question_title=question_title.replace("n","")
        question_title=question_title.replace("\\","")
        question_title=question_title=question_title.split("<")[0]
        return question_title

urls=[
"https://www.bitask.org/question/11438",
"https://www.bitask.org/question/11441",
"https://www.bitask.org/question/11443",
"https://www.bitask.org/question/11456",
"https://www.bitask.org/question/11469",
"https://www.bitask.org/question/11474",
"https://www.bitask.org/question/11484",
"https://www.bitask.org/question/11486",
"https://www.bitask.org/question/11489",
"https://www.bitask.org/question/11498",
"https://www.bitask.org/question/11530",
"https://www.bitask.org/question/11537",
"https://www.bitask.org/question/11554",
"https://www.bitask.org/question/11568",
"https://www.bitask.org/question/11593",
"https://www.bitask.org/question/11608",
"https://www.bitask.org/question/11609"
]
for one in urls:
    page = getPage(one)
    title=getQuestionTitle(page)
    print("[%s][%s]" %(title, one))
    
    
    