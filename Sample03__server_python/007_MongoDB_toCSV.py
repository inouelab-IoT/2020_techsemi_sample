import pandas as pd
from pymongo import MongoClient

gcpusername = "YOURE_GCP_USER_NAME" #GCPのユーザ名
# mongoDB 設定
dbname = gcpusername + 'DB' #Your DB name
collectionname = 'mqtt_log'

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))
    print(df)
    # Delete the _id
    if no_id and '_id' in df:
        del df['_id']

    return df

if __name__ == '__main__':
    df = read_mongo(dbname, collectionname, {'topic':gcpusername + '/GPS'})
    df.to_csv('1.csv', index=False)