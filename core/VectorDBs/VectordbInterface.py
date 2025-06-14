from abc import ABC, abstractmethod

class VectorDB(ABC):

    @abstractmethod
    def add_to_collection(self, documents: list[str]) -> None:
        pass

    @abstractmethod
    def get_query_to_collection(self, embeddings: list[float]) -> dict:
        pass