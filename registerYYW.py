# -*- coding: UTF-8 -*-
import random
import os
import json
import time
import sys
import io

sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def GetRandomName():
    account_name=""
    account_name=account_name+random.choice("abcdefghijklmnopqrstuvwxyz")
    account_name=account_name+random.choice("abcdefghijklmnopqrstuvwxyz")
    account_name=account_name+random.choice("abcdefghijklmnopqrstuvwxyz")
    account_name=account_name+random.choice("abcdefghijklmnopqrstuvwxyz")
    account_name=account_name+random.choice("abcdefghijklmnopqrstuvwxyz")
    account_name=account_name+random.choice("abcdefghijklmnopqrstuvwxyz")
    account_name=account_name+random.choice("abcdefghijklmnopqrstuvwxyz")
    account_name=account_name+random.choice("0123456789")
    account_name=account_name+random.choice("0123456789")
    account_name=account_name+random.choice("0123456789")
    return account_name

list_of_accounts=[]
with open("keys.txt","r",encoding='utf-8') as cf:
    for line in cf:
        register_account=[]
        key_pair=line.split(",")
        print(key_pair[0])
        register_info={}
        register_info["account"]={}
        register_info["account"]["secondary_key"]=key_pair[0]
        register_info["account"]["owner_key"]=key_pair[0]
        register_info["account"]["active_key"]=key_pair[0]
        register_info["account"]["memo_key"]=key_pair[0]
        register_info = str(json.dumps(register_info))
        
        cmd = "curl \"https://faucet.yoyow.org/api/v1/createAccount\" -H \"Origin: https://wallet.yoyow.org\" -H \"Accept-Encoding: gzip, deflate, br\" -H \"Accept-Language: zh-CN,zh;q=0.9\" -H \"User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5083.400 QQBrowser/10.0.972.400\" -H \"Content-type: application/json\" -H \"Accept: application/json\" -H \"Referer: https://wallet.yoyow.org/\" -H \"Connection: keep-alive\" --data-binary '" +register_info +"' -k --compressed"
        
        print(cmd)
        #break 
        
        
        
        yoyow_uid=""
        ret=os.popen(cmd)
        ret=ret.readlines()
        print(ret)
        ret = json.loads(ret[0])
        yoyow_uid=str(ret["data"])
        print(yoyow_uid)
        
        with open("register_accounts.txt","a",encoding='utf-8') as cf:
            record = yoyow_uid + "," + key_pair[0] + "," + key_pair[1] + "\n"
            cf.write(record)
        
        time.sleep(1805)
        
         