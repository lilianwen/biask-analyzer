在yoyow_client命令行里输入
get_relative_account_history 375867735 null 1 200 0
查询币问官方yoyow账号375867735的转账记录。
然后把获取到的批量转账记录适当修建保存到yoyow_transfer.txt文件里去。格式为：
Transfer 14.44110 YOYO from 375867735 to 465270071 -- could not decrypt memo   (Fee: 0.20898 YOYO) 

然后运行analyze.py脚本就能得到想要的结果了。