#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import boto3
from botocore.exceptions import ClientError
import os
from ast import literal_eval

# file open
gcpusername = "YOURE_GCP_USER_NAME" #GCPのユーザ名
MQTT_FILE = "home/"+ gcpusername + "/002_AWSIoT/aws_iot_mqtt.json"
mqtt_broker = open(MQTT_FILE).read()
mqtt_dict = literal_eval(mqtt_broker)

# 認証情報取得 
clientId = mqtt_dict['CLIENT_ID']
accessId = mqtt_dict['ACCESS_ID']
secretKey = mqtt_dict['SECRET_KEY']

try:
    bucketname = "ediot"
    KeyPrefix = clientId + "/"
    resource = boto3.resource(
        's3',
        region_name='ap-northeast-1',
        # Hard coded strings as credentials, not recommended.
        aws_access_key_id=accessId,
        aws_secret_access_key=secretKey
    )
except ClientError as e:
        logging.error(e)
        
bucket = resource.Bucket(bucketname)
objs = bucket.meta.client.list_objects_v2(Bucket=bucket.name, Prefix=KeyPrefix)
for o in objs.get('Contents'):
    key = o.get('Key')
    if key[-4:]=='.jpg':
        print(key)
        bucket.download_file(key, os.path.basename(key)) # download

#download
#bucket.upload_file('DownloadするS3のpath', '保存先のpath')

#upload
#bucket.upload_file('UPするファイルのpath', '保存先S3のpath')