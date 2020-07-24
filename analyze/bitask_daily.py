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

def save2file(file, context):
    with open(file,"w",encoding='utf-8') as cf:
        cf.write(context)
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
        question_title=question_title.replace(" ","")
        question_title=question_title.replace("\t","")
        question_title=question_title.replace("\n","")
        #question_title=question_title.replace("\\","")
        question_title=question_title=question_title.split("<")[0]
        return question_title
        
answer_times={}  
question_times={}  
anonymous_question_num=0
def analyzePage(page):
    #save2file("page.txt", page)
    global anonymous_question_num
    question_author_pos=page.find("<h3>发起人", 0)
    #print("question_author_pos=%d" %question_author_pos)
    if question_author_pos != -1:
        question_author_pos=page.find("pull-left", question_author_pos+1)
        question_author_pos=page.find("pull-left", question_author_pos+1)
        question_author_pos=page.find("aw-user-name", question_author_pos+1)
        question_author_pos=page.find(">", question_author_pos+1)
        question_author=page[question_author_pos+1:question_author_pos+50]
        question_author=question_author.split("<")[0]
        if question_author in question_times:
            question_times[question_author] +=1
        else:
            question_times[question_author]=1 
    else:
        anonymous_question_num +=1
    pos=0
    answer_user_num=0
    max_agree_n=0
    agree_max=[]
    while True:
        pos=page.find("answer_list",pos)
        if pos != -1:
            answer_user_num +=1
            pos +=1
            #回答者昵称
            #print(pos)
            pos_user_name=page.find("aw-user-name", pos)
            #pos_user_name=page.find("BTS", pos)
            #pos_user_name=page.find("<a href",pos_user_name+1)
            #pos_user_name=page.find("<a href",pos_user_name+1)
            pos_user_name=page.find(">",pos_user_name+1)
            user_name=page[pos_user_name+1:pos_user_name+50]
            #print(user_name)
            user_name=user_name.split("<")[0]
            #print(pos_user_name)
            print(user_name)
            
            if user_name in answer_times:
                answer_times[user_name] += 1
            else:
                answer_times[user_name] = 1
            
            
            pos_agree=page.find("icon-agree", pos)
            agree_n=page[pos_agree+61:pos_agree+70]
            #print(page[pos_agree+61:pos_agree+70])
            agree_n=int(agree_n.split("<")[0])
            #print(pos_agree)
            print(agree_n)
            
            if agree_n >= max_agree_n:
                agree_max=[]
                agree_max.append(user_name)
                agree_max.append(agree_n)
                max_agree_n=agree_n
            
            '''
            pos_disagree=page.find("icon-disagree", pos)
            disagree_n=page[pos_disagree:pos_disagree+570]
            #print(disagree_n)
            break
            
            pos_comment=page.find("operate", pos)
            user_name=page[pos_comment:pos_comment+570]
            print(pos_comment)
            
            print("=================")
            
            #print(agree_str.split("<")[0])
            #agree_num=int(agree_str.split("<")[0])
            #print(agree_num)
            
            
            #被赞数
            #被踩数
            #被回复数
            '''
            
        else:
            break
    return answer_user_num,agree_max
#print(getPage("https://www.bitask.org/question/7912"))

info=[]
start_index = 11610
i = start_index
error_num=0
delete_question_num=0
zero_answer_questions=[]
sum_aw_num=0
questions_url={}
while True:
    print(i)
    url = "https://www.bitask.org/question/%d" %i
    status_code, html=getPage(url)
    #if i==11613:
    #    break
    if status_code == 404:
        error_num +=1
        delete_question_num +=1
        if error_num == 30:
            break
        else:
            i+=1
            continue
    elif status_code == 200:
        error_num=0
        #分析有多少个用户评论了，多少个人赞了，多少人踩了
        questions_url[url]=getQuestionTitle(html)
        print(questions_url[url])
        aw_num,agree_max=analyzePage(str(html))
        sum_aw_num +=aw_num
        if aw_num !=0:
            one_page=[]
            one_page.append(i)
            one_page.append(aw_num)
            one_page.append(agree_max)
            info.append(one_page)
        else:
            zero_answer_questions.append(url)
            
        
    i+=1
stop_index = i-30+1
delete_question_num = delete_question_num-30
max_aw_num=0
max_aw_num_list=[]
max_agree_num=0
max_agree_list=[]
print(info)
for one in info:
    print(one)
    if max_aw_num < one[1]:
        max_aw_num_list=one
        max_aw_num=one[1]
        
    if max_agree_num < one[2][1]:
        max_agree_list=one
        max_agree_num=one[2][1]

question_num=stop_index-start_index
print("今日最佳：")
print("今日共创建提问数：%d,共有%d次回答创建的问题,平均每个新问题被回答次数%f" %(question_num, sum_aw_num, 1.0*sum_aw_num/question_num))
url="https://www.bitask.org/question/%d " % max_aw_num_list[0]      
print("今日回复人数最多的提问是：%s[回复人数%d]" %(url, max_aw_num_list[1]))  
url="https://www.bitask.org/question/%d " % max_agree_list[0]  
print("今日点赞人数最多的回答是：%s[作者：%s,  点赞数%d]" %(url, max_agree_list[2][0], max_agree_list[2][1]))
print("今日被管理员删除的新创建的提问数量：%d" %delete_question_num)        
#参与提问和回答的总人数
#把所有人的昵称都放到一个set里面，然后查看set里面的数据量，现在还缺提问者的昵称
#查看谁提问+回答问题的次数最多

print("匿名提问的数量:%d" %anonymous_question_num)
max_answer_times=0
max_answer_people=""
for one in answer_times:
    if answer_times[one] > max_answer_times:
        max_answer_times = answer_times[one]
        max_answer_people=one
print("今日回答新创建的问题次数最多的人是【%s】,回答次数:%d" %(max_answer_people, max_answer_times))

max_question_times=0
max_question_people=""        
for one in question_times:
    if question_times[one] > max_question_times:
        max_question_times = question_times[one]
        max_question_people = one
print("今日创建新问题次数最多的人是【%s】,提问次数:%d" %(max_question_people, max_question_times))
        
print("今日零回复的问题数：%d" %(len(zero_answer_questions)))
print("今日零回复的问题列表如下：")
for one in zero_answer_questions:
    code, page = getPage(one)
    title=getQuestionTitle(page)
    print("[%s][%s]" %(title, one))
    
with open("news.txt","w",encoding='utf-8') as cf:
    for one in questions_url:
        #record="["+str(questions_url[one])+"]"+"["+one+"]\n"
        record="[%s][%s]\n" %(questions_url[one], one)
        cf.write(record)    


#总共的提问数量
#最多回答数
#最多的点赞问题，谁提供的
#最多的踩的问题，谁提供的

