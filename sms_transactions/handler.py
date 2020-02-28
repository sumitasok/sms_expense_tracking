from pymongo import MongoClient
import os
import bson
import re
import datetime

hdfcCreditCardInterpreterFormatStr = '%Y-%m-%d:%H:%M:%S'

# ALERT: You've spent Rs.5605.00  on CREDIT Card xx3690 at AARKITHA on 2020-02-22:12:09:36.Avl bal - Rs.286107.00, curr o/s - Rs.13893.00.Not you? Call 18002586161.
def hdfcCreditCardInterpreter(txn):
    x = re.search("ALERT: You\'ve spent Rs.([0-9.]+)\s+on\s+([a-zA-Z0-9\s._]+)? on (\d{4}-\d{2}-\d{2}:\d{2}:\d{2}:\d{2}).Avl bal - Rs.([0-9.]+), curr o\/s - Rs.([0-9]+.[0-9]+).", txn)
    return {
        'expense_amount': float(x.group(1)),
        'payment_mode': x.group(2).split('at', 1)[0].strip(),
        'merchant': x.group(2).split('at', 1)[1].strip(),
        'datetime': datetime.datetime.strptime(x.group(3), hdfcCreditCardInterpreterFormatStr),
        'available_balance': float(x.group(4)),
        'outstanding_amount': float(x.group(5))
    } if x != None else {}

# ALERT:You've spent Rs.428.00 on CREDIT Card xx3690 at FRESHTOH3631510 in BANGALORE on 2020-02-15:16:46:51.Not you?Call 18002586161.
def hdfcCreditCardInterpreter2(txn):
    x = re.search("ALERT:You\'ve spent Rs.([0-9.]+)\s+on\s+([a-zA-Z0-9\s._//]+)? on (\d{4}-\d{2}-\d{2}:\d{2}:\d{2}:\d{2}).", txn)
    return {
        'expense_amount': float(x.group(1)),
        'payment_mode': x.group(2).split('at', 1)[0].strip(),
        'merchant': x.group(2).split('at', 1)[1].strip(),
        'datetime': datetime.datetime.strptime(x.group(3), hdfcCreditCardInterpreterFormatStr)
    } if x != None else {}

# ALERT:You've spent Rs.3638.00 via Debit Card xx6504 at www.lenskart.c on 2019-01-14:20:29:59.Avl Bal Rs.264666.51.Not you?Call 18002586161.
def hdfcCreditCardInterpreterVia(txn):
    x = re.search("ALERT:You\'ve spent Rs.([0-9.]+)\s+via\s+([a-zA-Z0-9\s._//]+)? on (\d{4}-\d{2}-\d{2}:\d{2}:\d{2}:\d{2}).", txn)
    return {
        'expense_amount': float(x.group(1)),
        'payment_mode': x.group(2).split('at', 1)[0].strip(),
        'merchant': x.group(2).split('at', 1)[1].strip(),
        'datetime': datetime.datetime.strptime(x.group(3), hdfcCreditCardInterpreterFormatStr)
    } if x != None else {}

def mongoCollection(connstr, db, collection):
    client = MongoClient(connstr)
    db = client[db]
    return db[collection]


def main(event, context):
    print(os.environ.get('MONGODB_CONN_STR'))
    collection = mongoCollection(os.environ.get('MONGODB_CONN_STR'), 'smsinfo', 'transactions')

    for _item in list(
    enumerate(
        collection.find({
            "message.text": {'$regex': 'ALERT: You\'ve spent Rs.([0-9.]+)'}
            }).sort([("message.date",1)]))):
        print("message", _item[1])

def extract_populate(event, context):
    collection = mongoCollection(os.environ.get('MONGODB_CONN_STR'), 'smsinfo', 'transactions')

    for _item in list(
        enumerate(
            collection.find({
                "message.text": {'$regex': 'ALERT: You\'ve spent Rs.([0-9.]+)'},
                "status.analysis_done": {'$ne': True}}
            ).sort([("message.date",1)]))):
        print("message", _item[1])
        _transaction = hdfcCreditCardInterpreter(_item[1]['message']['text'])
        print("analysis", _transaction, "\n\n")
        result = collection.update_one(
            {'_id': bson.ObjectId(str(_item[1]['_id']))},
            {'$set' : {'transaction': _transaction, 'status': {'analysis_done': True}}})
        print('success' if result.modified_count == 1 else 'unsuccessful')
    
    for _item in list(
        enumerate(
            collection.find({
                "message.text": {'$regex': 'ALERT:You\'ve spent Rs.([0-9.]+) on'},
                "status.analysis_done": {'$ne': True}} #             
            ).sort([("message.date",1)]))):
        print("message", _item[1])
        _transaction = hdfcCreditCardInterpreter2(_item[1]['message']['text'])
        print("analysis", _transaction, "\n\n")
        if _transaction != {}:
            result = collection.update_one(
                {'_id': bson.ObjectId(str(_item[1]['_id']))},
                {'$set' : {'transaction': _transaction, 'status': {'analysis_done': True}}})
            print('success' if result.modified_count == 1 else 'unsuccessful')
        
    for _item in list(
        enumerate(
            collection.find({
                "message.text": {'$regex': 'ALERT:You\'ve spent Rs.([0-9.]+) via'},
                "status.analysis_done": {'$ne': True}}
            ).sort([("message.date",1)]))):
        print("message", _item[1])
        _transaction = hdfcCreditCardInterpreterVia(_item[1]['message']['text'])
        print("analysis", _transaction, "\n\n")
        if _transaction != {}:
            result = collection.update_one(
                {'_id': bson.ObjectId(str(_item[1]['_id']))},
                {'$set' : {'transaction': _transaction, 'status': {'analysis_done': True}}})
            print('success' if result.modified_count == 1 else 'unsuccessful')

if __name__ == "__main__":
    extract_populate('', '')