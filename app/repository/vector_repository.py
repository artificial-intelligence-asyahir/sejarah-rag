import os

from qdrant_client.http.models import PointStruct
from qdrant_client import models
from app.repository.qdrant import connection

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")
TOP_K = os.getenv("QDRANT_TOP_K")

class VectorRepository:
    def __init__(self, collection_name: str = COLLECTION_NAME, top_k: int = TOP_K):
        self.client = connection
        self.collection_name = collection_name
        self.top_k = top_k

    def create_collection(self, size: int, distance: models.Distance):
        self.client.create_collection(collection_name=self.collection_name,
                                      vectors_config=models.VectorParams(size=size,
                                                                         distance=distance))


    def save_vector(self, points: list[PointStruct]):
        operation_info = self.client.upsert(collection_name=self.collection_name,
                           wait=True,
                           points=points)
        print(operation_info)

    def search_vector(self, query: list[float]):
        return self.client.query_points(collection_name=self.collection_name,
                                        query=query,
                                        with_payload=True,
                                        limit=self.top_k)

