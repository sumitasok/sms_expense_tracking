import sqlite3
from sqlite3 import Error

import os

import pymongo

import time

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()
 
def select_sms(conn, filters):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    date = filters['date']
    cur.execute("SELECT text, date, guid FROM message where (text LIKE '%deliver%')" + " and date > %d" %(date,))
 
    rows = cur.fetchall()
 
    for row in rows:
        yield {'text': row[0], 'date': row[1], 'guid': row[2]}

import datetime

def date_string_from_integer(i):
    # return datetime.strptime(str(i), '%Y%m%d')
    # return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(str(i)[0:9]+'.'+str(i)[10:17])))
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i-621355968000000000))
    # return str(time.gmtime(float(str(i)[:-6]+'.'+str(i)[-6:])))

from pymongo import MongoClient

def mongoCollection(connstr, db, collection):
    client = MongoClient(connstr)
    db = client[db]
    return db[collection]


if __name__ == '__main__':
    conn = create_connection("/data/chat.db")

    collection = mongoCollection(os.environ.get('MONGODB'), 'smsinfo', 'delivery')
    latestObjList = list(enumerate(collection.find().sort([("message.date",-1)]).limit(1)))
    if len(latestObjList) == 0:
        date = 0
    else:
        date = latestObjList[0][1]['message']['date']

    for value in select_sms(conn, {'date': date}):
        obj = collection.find_one({'message': {'guid': value['guid']}})
        print(value)
        if obj == None:
            print(collection.insert_one({ 'message' : value }).inserted_id)
        else:
            print('already exist')