from abc import ABC, abstractmethod
from Queries.UserQueryInterface import UserQuery

class Embedder(ABC):

    @abstractmethod
    def create_embeddings(self, query: UserQuery) -> list[float]:
        pass