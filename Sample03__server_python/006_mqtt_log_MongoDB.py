#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

import boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from ast import literal_eval
from datetime import datetime
import time
import json

# file open
gcpusername = "YOURE_GCP_USER_NAME" #GCPのユーザ名
MQTT_FILE = "home/"+ gcpusername + "/002_AWSIoT/aws_iot_mqtt.json"
mqtt_broker = open(MQTT_FILE).read()
mqtt_dict = literal_eval(mqtt_broker)

# 認証情報取得 
clientId = mqtt_dict['CLIENT_ID']
endPoint = mqtt_dict['ENDPOINT']
mqttport = mqtt_dict['PORT'] # Cognito経由の認証では、Websocket SigV4　しか使用できない
rootCA = mqtt_dict['ROOT_CA']
accessId = mqtt_dict['ACCESS_ID']
secretKey = mqtt_dict['SECRET_KEY']

#topic
topic = clientId + "/#"

# mongoDB 設定
mongohost = '127.0.0.1'
mongoport = 27017
db = clientId + 'DB' #Your DB name
#コネクション作成
mongoclient = MongoClient(mongohost, mongoport)
#データベースからtestコレクションを取得
col = mongoclient[db]['mqtt_log']


#Subscribe
def onSubscribe(client, userdata, message):
    print("= Subscribe ========================")
    print("message:{} topic:{}".format(message.payload, message.topic))
    print("topic: " + message.topic)
    print("payload: " + str(message.payload.decode('utf-8')))
    payload_DICT = json.loads(message.payload.decode('utf-8'))
    payload_DICT["topic"] = message.topic
    print(payload_DICT)
    col.insert_one(payload_DICT)
    print("====================================")

#Main
def main():
    mqttclient = AWSIoTMQTTClient(clientId, useWebsocket=True) # Websocket SigV4を利用
    mqttclient.configureIAMCredentials(accessId, secretKey)
    mqttclient.configureCredentials(rootCA) # ルート証明書の設定が必要
    mqttclient.configureEndpoint(endPoint, mqttport)
    mqttclient.configureAutoReconnectBackoffTime(1, 32, 20)
    mqttclient.configureOfflinePublishQueueing(-1)
    mqttclient.configureDrainingFrequency(2)
    mqttclient.configureConnectDisconnectTimeout(10)
    mqttclient.configureMQTTOperationTimeout(5)
    mqttclient.connect()
    print("onConnect")
    mqttclient.subscribe(topic, 1, onSubscribe)
    while True:
        time.sleep(5)

if __name__ == '__main__':
    main()