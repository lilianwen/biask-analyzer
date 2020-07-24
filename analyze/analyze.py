# -*- coding: UTF-8 -*-
import random
import os
import json
import time
import sys
import io

import numpy.random as npr
import matplotlib.pyplot as plt
import xlwt

name_yoyow_map={}
with open("account_map.txt","r",encoding='utf-8') as cf:
    for line in cf:
        line=line.replace("\n","")
        account_map=line.split(" ")
        name=account_map[0]
        yoyow=account_map[1]
        name_yoyow_map[yoyow]=name
        
print(name_yoyow_map)

record_list=[]
amount_list=[]
sum=0
with open("yoyow_transfer.txt","r",encoding='utf-8') as cf:
    for line in cf:
        transfer_record=line.split(" ")
        yoyow=transfer_record[6]
        amount=transfer_record[1]
        #print("%s %s" %(yoyow,amount))
        amount_list.append(float(amount))
        sum += float(amount)
        one_record=[]
        one_record.append(yoyow)
        one_record.append(float(amount))
        record_list.append(one_record)
account_num=len(amount_list)


n, bins, patches = plt.hist(amount_list,bins=400,normed=1, histtype="stepfilled")
record_list.sort(key=lambda x:x[1], reverse=True)#lambda x:x[1]返回list的第二个数据
print(record_list)

i=1
top_sum=0
for one in record_list:
    if one[0] in name_yoyow_map:
        one[0]=name_yoyow_map[one[0]]
    print("[%d][%s][%f yoyow]" %(i, one[0], one[1]))
    if i<= account_num*0.2:
        top_sum += one[1]
    i +=1
#print(amount_list)
print("奖励yoyow总数: %f" %sum)
print("奖励用户总数: %d" %account_num)
print("奖励最多yoyow数: %f" %(max(amount_list)))
print("奖励最少yoyow数: %f" %(min(amount_list)))
print("奖励yoyow平均数: %f" %(sum/account_num))
print("头部20%%的用户收入总和(%f yoyow)占总收入的%f%%" %(top_sum, 100*top_sum/sum))

work_book = xlwt.Workbook() #创建工作簿
sheet1 = work_book.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建shee
row=0
for one in record_list:
    sheet1.write(row,0,one[0])
    sheet1.write(row,1,one[1])
    row +=1
work_book.save('bitask.xls')#保存文件
    

plt.show()   
     
