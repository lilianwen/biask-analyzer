# -*- coding: UTF-8 -*-
import os
import sys
import re
import urllib.request;
import json
import socket
import random
import time
from grapheneapi import grapheneapi 
import pymysql



def getTransfer(blockHeight):
    _rpc_ro   = grapheneapi.GrapheneAPI("127.0.0.1", 8091, "", "")
    ret=_rpc_ro.get_block(blockHeight)
    print(ret)
    if ret["transaction_ids"]:
        print("ids:")
        print(ret["transaction_ids"])
        
        print("timestamp:")
        print(ret["timestamp"])
        
        print("transactions:")
        
        result=[]
        i=0
        while i < len(ret["transaction_ids"]):
            one_transfer=[]
            if ret["transactions"][i]["operations"][0][0]==0:
                print(ret["transactions"][i]["operations"][0][1]["from"])
                print(ret["transactions"][i]["operations"][0][1]["to"])
                print(ret["transactions"][i]["operations"][0][1]["amount"]["amount"])
                print(ret["transactions"][i]["operations"][0][1]["amount"]["asset_id"])
                
                one_transfer.append(ret["transactions"][i]["operations"][0][1]["from"])
                one_transfer.append(ret["transactions"][i]["operations"][0][1]["to"])
                one_transfer.append(int(ret["transactions"][i]["operations"][0][1]["amount"]["amount"]))
                one_transfer.append(int(ret["transactions"][i]["operations"][0][1]["amount"]["asset_id"]))
                
                result.append(one_transfer)
            i +=1
        return result

def main():
    #for i in range(1, 100):
    #    getTransfer(i)
    conn = pymysql.connect( host='localhost',port=3306, user='root',passwd='123456',db='yoyow',charset='utf8' )
    cur  = conn.cursor();
    
    sql_insert = 'INSERT INTO `transfer`VALUES(0,%s,%s,%s,%s)'

    #ret=getTransfer(8366018)
    for i in range(8600000, 8700000):
        time.sleep(0.01)
        ret=getTransfer(i)
        if ret:
            print(ret)
            for one in ret:
                cur.execute(sql_insert, (one[0],one[1],one[2],one[3]))
            conn.commit()
        
        print("finish block %d" %i)
    cur.close()
    conn.close()
    
if __name__ == "__main__":
    main()