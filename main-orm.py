from pymodm.connection import connect
import os
import bson

connect(os.environ.get('MONGODB_CONN_STR'), alias="smsinfo")


from pymongo.write_concern import WriteConcern

from pymodm import MongoModel, fields, EmbeddedMongoModel

class Data(EmbeddedMongoModel):
    _id=fields.ObjectIdField(primary_key=True)
    text=fields.CharField()

    class Meta:
        final=True


class Sample(MongoModel):
    _id=fields.ObjectIdField(primary_key=True)
    data=fields.EmbeddedDocumentField(Data)

    class Meta:
        connection_alias='smsinfo'
        collection_name='sample'
        final=True


# d = Data(_id=bson.ObjectId(), text='data')
# s = Sample(_id=bson.ObjectId(), data=d).save()

class Message(EmbeddedMongoModel):
    text=fields.CharField()
    date=fields.IntegerField()
    guid=fields.UUIDField()

class Status(EmbeddedMongoModel):
    ignore=fields.BooleanField()
    run_id=fields.CharField()
    analysis_done=fields.BooleanField()

class Transaction(EmbeddedMongoModel):
    expense_amount=fields.FloatField()
    payment_mode=fields.CharField()
    merchant=fields.CharField()
    datetime=fields.DateTimeField()
    available_balance=fields.FloatField()
    outstanding_amount=fields.FloatField()
    category=fields.CharField()
    sub_category=fields.CharField()


from pymodm.manager import Manager
class SmsInfoManager(Manager):
    def get_by_id(self, _id):
        return self.model.objects.get({'_id': _id})

class SmsInfo(MongoModel):
    _id=fields.ObjectIdField(primary_key=True)
    message=fields.EmbeddedDocumentField(Message)
    status=fields.EmbeddedDocumentField(Status)
    transaction=fields.EmbeddedDocumentField(Transaction)

    objects = SmsInfoManager()

    class Meta:
        connection_alias='smsinfo'
        collection_name='transactions'
        final=True



for post in SmsInfo.objects.raw({'status.analysis_done': True}).limit(10).only('_id', 'message', 'status', 'transaction'):
    print('post content: ' + repr(post))