from pymongo import MongoClient

URI = "mongodb://asyahir:password@localhost:27017"
DATABASE_NAME = "sejarah_db"

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




