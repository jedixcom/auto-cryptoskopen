#mongo_utils.py
import os
import pymongo

def connect_to_mongo():
    mongo_uri = os.getenv('MONGO_URI')
    try:
        client = pymongo.MongoClient(mongo_uri)
        db = client["cryptoskopen-eu"]
        print("Successfully connected to MongoDB")
        return client, db
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(f"Error connecting to MongoDB: {err}")
        exit(1)