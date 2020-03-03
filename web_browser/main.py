from flask import Flask, flash, redirect, render_template, request, session, abort
app = Flask(__name__)

from pymongo import MongoClient
import os
import bson

def mongoCollection(connstr, db, collection):
    client = MongoClient(connstr)
    db = client[db]
    return db[collection]

import re
import datetime

collection = mongoCollection(os.environ.get('MONGODB_CONN_STR'), 'smsinfo', 'transactions')

def extract_transactions(i):
    keys = ['expense_amount', 'payment_mode', 'merchant', 'datetime', 'category', 'sub_category']
#     return list(i[1]['transaction'].values()) + [str(i[1]['_id'])]
    return [i[1]['transaction'].get(key, None) for key in keys] + [str(i[1]['_id'])]



@app.route("/month/<int:month>")
def index(month):
    year = 2020
    month = month

    next_month = 1 if month == 12 else month + 1
    next_year = year + 1 if month == 12 else year

    monthly = list(enumerate(collection.find({'status': {'analysis_done': True},
                    'transaction.datetime' : {
                        '$gte': datetime.datetime(year,month,1), '$lt': datetime.datetime(next_year,next_month,1)}
                    }, {'transaction': 1})))

    monthly_transactions = list(map(extract_transactions, monthly))
    return render_template(
        'index.html',monthly_transactions=monthly_transactions)

@app.route("/delete/<string:_id>")
def delete(_id):
    r = collection.delete_one({_id: bson.ObjectId(_id)})
    print("delete " + str(r.deleted_count))
    return redirect('/month/1')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)