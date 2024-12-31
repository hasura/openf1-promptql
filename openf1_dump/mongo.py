import os
from pymongo import MongoClient

def get_db():
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    client = MongoClient(mongo_url)
    db = client["openf1-dump"]
    return db

def get_collection(name):
    return get_db()[name]