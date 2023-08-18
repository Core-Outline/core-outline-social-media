from pymongo import MongoClient
from bson.objectid import ObjectId

from config.database_config import db_username, db_password, db_database


def createClient():
    client = MongoClient(
        f'mongodb+srv://{db_username}:{db_password}@cluster0.rfams.mongodb.net')

    return client[db_database]


def create(db, collection, document):
    output = db[collection].insert_one(document)
    return {"_id": str(output.inserted_id)}


def get(db, collection, condition):
    obj = db[collection].find_one({'_id': ObjectId(condition['_id'])})
    print(obj)
    return {**obj, "_id": str(obj['_id'])}


def fetch(db, collection, array_of_conditions):
    docs = db[collection].find(array_of_conditions)
    return [{**doc, "_id": str(doc['_id'])} for doc in docs]


def update(db, collection, document):
    return db[collection].find_one_and_update(
        {'_id': ObjectId(document._id)}, document)
