#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient
from datetime import datetime

host = '127.0.0.1'
port = 27017
db = 'DB_name' #Your DB name
#コネクション作成
client = MongoClient(host, port)

#データベースからtestコレクションを取得
col = client[db]['test']


print("========find_one========")
print(col.find_one())

print("========find========")
for data in col.find():
    print(data)

print("========find_query========")
for data in col.find({u'a':10}):
    print(data)