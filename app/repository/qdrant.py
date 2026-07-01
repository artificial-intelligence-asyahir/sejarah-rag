import os

from qdrant_client import QdrantClient

URL = os.getenv("QDRANT_URL")

class QdrantConnector:
    _instance: QdrantClient | None = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = QdrantClient(url=URL)
            except Exception as e:
                print(f"Error connecting to Qdrant: {e}")
                raise
        return cls._instance

connection = QdrantConnector()

