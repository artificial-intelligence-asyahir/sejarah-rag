from qdrant_client import QdrantClient

URL = "http://127.0.0.1:6333"

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

