from pymongo import MongoClient

class Collection:
    def __init__(self, connection_str=None, db_name=None, collection_name=None):
        self._client = MongoClient(connection_str)
        self._db = self._client[db_name]
        self._collection_name = collection_name

    def collection(self):
        return self._db[self._collection_name]

class MessageQuery:
    def __init__(self, connection = None):
        self._collection = connection.collection

    def non_analysed_message_text_by_regex(self, regex_str = None):
        return self._collection().find({
                "message.text": {'$regex': regex_str},
                "status.analysis_done": {'$ne': True}}
            ).sort([("message.date",1)])

class HdfcCCInterpreter: