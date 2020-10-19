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

#データの更新
col.insert({'b' : 10})

for data in col.find({'b':10}):
    print(data)