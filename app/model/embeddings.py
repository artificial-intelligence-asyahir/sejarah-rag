from sentence_transformers import SentenceTransformer
from app.model.base import SingletonMeta

class EmbeddingModel(metaclass=SingletonMeta):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, text: str):
        return self.model.encode(text)

class CrossEncoderModel:
    def __init__(self):
        self.model = SentenceTransformer("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def get_ranking(self, query: str, corpus: list[str]):
        return self.model.predict(query, corpus)




