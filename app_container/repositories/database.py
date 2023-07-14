from pymongo import MongoClient
from bson.objectid import ObjectId

from config.database_config import db_username, db_password, db_database


def createClient():
    client = MongoClient(
        f'mongodb+srv://{db_username}:{db_password}@cluster0.rfams.mongodb.net')

    return client[db_database]


def create(db, collection, document):
    output = db[collection].insert_one(document)
    return output.inserted_id


def get(db, collection, condition):
    return db[collection].find_one({'_id': ObjectId(condition['_id'])})


def fetch(db, collection, conditions):
    docs = db[collection].find(conditions)
    return [doc for doc in docs]
