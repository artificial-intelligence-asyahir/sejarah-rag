import os

from pymongo import MongoClient

URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("MONGO_DB_NAME")

class MongoDatabaseConnector:
    _instance: MongoClient | None = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = MongoClient(URI)
            except Exception as e:
                print(f"Error connecting to MongoDB: {e}")
                raise
        return cls._instance


connection = MongoDatabaseConnector()




