from abc import ABC, abstractmethod
from Queries.UserQueryInterface import UserQuery
from Embedders.EmbedderInterface import Embedder
from VectorDBs.VectordbInterface import VectorDB

class Retriever(ABC):

    @abstractmethod
    def retrieve_relevant_chunks(self, top_k: int) -> list[str]:
        pass