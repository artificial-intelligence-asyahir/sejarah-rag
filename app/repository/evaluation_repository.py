from app.repository.mongodb import connection, DATABASE_NAME


class EvaluationRepository:
    def __init__(self, collection_name: str):
        self.evaluation = None
        self.db = connection.get_database(DATABASE_NAME)
        self.collection_name = self.collection_name

    def create_collection(self):
        if self.collection_name not in self.db.list_collection_names():
            self.db.create_collection(self.collection_name)

        self.evaluation = self.db[self.collection_name]

