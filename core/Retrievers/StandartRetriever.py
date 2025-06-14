from Retrievers.RetrieverInterface import Retriever
from Queries.UserQueryInterface import UserQuery
from VectorDBs.VectordbInterface import VectorDB
from Embedders.EmbedderInterface import Embedder

class StandartRetriever(Retriever):

    def __init__(
            self, 
            user_query: UserQuery,
            vector_db: VectorDB,
            embedder: Embedder
            ) -> None:
        self.user_query = user_query.get_user_query()
        self.vector_db = vector_db
        self.embedder = embedder

    def retrieve_relevant_chunks(self, top_k: int = 5):
        pass