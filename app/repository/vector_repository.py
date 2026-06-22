from qdrant_client.http.models import PointStruct

from app.repository.qdrant import connection

COLLECTION_NAME = 'sejarah_collection'

class VectorRepository:
    def __init__(self):
        self.client = connection

    def save_vector(self, points: list[PointStruct]):
        operation_info = self.client.upsert(collection_name=COLLECTION_NAME,
                           wait=True,
                           points=points)
        print(operation_info)

    def search_vector(self, query: list[float]):
        return self.client.query_points(collection_name=COLLECTION_NAME,
                                        query=query,
                                        with_payload=True,
                                        limit=7)

