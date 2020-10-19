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

data = col.find_one({'b':10})
data['b'] = 11
#データの更新
col.save(data)

for data in col.find({u'b':11}):
    print(data)
