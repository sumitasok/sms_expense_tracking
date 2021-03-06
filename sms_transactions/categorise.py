from pymongo import MongoClient
import os
import bson

def mongoCollection(connstr, db, collection):
    client = MongoClient(connstr)
    db = client[db]
    return db[collection]

def add_category_info_for_merchant(collection, merchant, category='', sub_category=''):
    result = collection.update_many(
        {'transaction.merchant': merchant, 'transaction.category': None}, 
        {'$set' : {'transaction.category': category, 'transaction.sub_category': sub_category}})
    print(str(merchant) + ' modified ' + str(result.modified_count))
    return result

merchant_category_mapping = [
    {'merchant': ['Uber', 'UBER'], 'category': 'taxi', 'sub_category': 'uber'},
    {'merchant': ['SWIGGY', 'zomato@hdfcbank', 'ZOMATO11120', 'Eat Fit', 'www.zomato.com', 'SWIGGYXL3549786', 'Paratha Corner', 'bharatpe.9040576993@icici', 'upiswiggy@icici', 'swiggyupi@axisbank'], 'category': 'food', 'sub_category': 'delivery'},
    {'merchant': ['..MATTO COFFEA_'], 'category': 'meet-up', 'sub_category': 'food'},
    {'merchant': ['bharatpe90200570491@yesbankltd', 'q22904860@ybl', 'bharatpe90200570491¡yesbankltd'], 'category': 'meet-up', 'sub_category': 'breakout'},
    {'merchant': ['NEW FRUIT LAND', 'NEW FRUITLAND'], 'category': 'grocery', 'sub_category': 'vegetables'},
    {'merchant': ['www.bigbasket.', 'M K RETAIL'], 'category': 'grocery', 'sub_category': 'all'},
    {'merchant': ['VIN*APPLE COM.', 'VSI*APPLE COM.'], 'category': 'subscription', 'sub_category': 'apps'},
    {'merchant': ['VPS*HORTICULT.'], 'category': 'grocery', 'sub_category': 'vegetables'},
    {'merchant': ['FRESHTOH3631510', 'FRESHTOH3631510 in BANGALORE', 'Freshtohome'], 'category': 'grocery', 'sub_category': 'non-veg'},
    {'merchant': ['AJIO', 'MYNTRA72883', 'FIRSTCRY11847'], 'category': 'purchase', 'sub_category': 'cloths'},
    {'merchant': ['IIN*Amazon .', 'AMAZON'], 'category': 'purchase', 'sub_category': 'household'},
    {'merchant': ['amazonsellerservices.98397377@hdfcbank'], 'category': 'purchase', 'sub_category': 'toiletry'},
    {'merchant': ['Solanki medicals'], 'category': 'medical', 'sub_category': 'medicine'},
    {'merchant': ['Bharti Airtel Limited', 'JIO Infocom'], 'category': 'utility', 'sub_category': 'mobile'},
    {'merchant': ['Instapay BBPS'], 'category': 'utility', 'sub_category': 'bescom'},
    {'merchant': ['LIC'], 'category': 'insurance', 'sub_category': 'insurance'},
    {'merchant': ['..RAJDHANI PHOENIX_', '..ARENA_', 'bharatpe09600003315¡yesbankltd', 'SRI UDUPI PARK'],
        'category': 'food', 'sub_category': 'eating-out'},
    {'merchant': ['The lassi club', 'paytmqr281005050101j1cog2ifqf2u@paytm'], 'category': 'food', 'sub_category': 'snacks'},
    {'merchant': ['H M LEISURE'], 'category': 'purchase', 'sub_category': 'toys'},
    {'merchant': ['PEPPERFRY64213'], 'category': 'purchase', 'sub_category': 'furniture'},
    {'merchant': ['HPCL HINDUSTAN PETROLE', 'HINDUSTAN PETROLEUM CO'], 'category': 'auto', 'sub_category': 'fuel'},
    {'merchant': ['vijualoor@okhdfcbank', 'cru5ty.d3m0nx-2@okhdfcbank'], 'category': 'others', 'sub_category': 'others'},
    {'merchant': ['BOOKMYSHOW'], 'category': 'entertainment', 'sub_category': 'movie'},
    {'merchant': ['PVR LIMITED.'], 'category': 'food', 'sub_category': 'movie'},
    {'merchant': ['PHOENIX MARKETCITY BAN'], 'category': 'auto', 'sub_category': 'parking'},
    {'merchant': ['Akshayakalpa'], 'category': 'grocery', 'sub_category': 'diary'},
    {'merchant': ['BBPSBILLPAY'], 'category': 'utility', 'sub_category': 'internet'},

]

# bharatpe09600003315¡yesbankltd => Empire hotel


def categorise(event, context):
    collection = mongoCollection(os.environ.get('MONGODB_CONN_STR'), 'smsinfo', 'transactions')

    pipeline = [
        {"$match": {
            "status.analysis_done": True,
            "transaction.category": {'$exists': True}
        }},
        {"$sort": {
            'message.date': -1,
        }},
        {"$project": {
            "_id": "$transaction.merchant",
            "merchant": "$transaction.merchant",
            "category": "$transaction.category",
            "sub_category": "$transaction.sub_category"
        }},
        {"$group": {
            '_id': '$merchant',
            'merchant': {
                '$last': '$merchant'
            },
            'category': {
                '$last': '$category'
            },
            'sub_category': {
                '$last': '$sub_category'
            }
        }}
    ]

    merchant_category_mapping = list(collection.aggregate(pipeline))
    for _m in merchant_category_mapping:
        add_category_info_for_merchant(collection, _m['merchant'], category=_m['category'], sub_category=_m['sub_category'])
        # for _merchant in _m['merchant']:
        #     add_category_info_for_merchant(collection, _merchant, category=_m['category'], sub_category=_m['sub_category'])


if __name__ == "__main__":
    categorise('', '')