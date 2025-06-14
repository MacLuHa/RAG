from Embedders.EmbedderInterface import Embedder
from Queries.UserQueryInterface import UserQuery
from sentence_transformers import SentenceTransformer
from typing import List

class SentenceTransformerEmbedder(Embedder):
    """
    An embedder that uses a SentenceTransformer model to create vector embeddings
    from user queries.
    """
    def __init__(self, model: str = 'all-MiniLM-L6-v2') -> None:
        """
        Initializes the SentenceTransformer model.

        Args:
            model (str): The name or path of the pre-trained sentence transformer model.
        """
        self.model = model
        self.embedder = SentenceTransformer(self.model)

    def create_embeddings(self, query: UserQuery) -> List[float]:
        """
        Creates embeddings from a user query using the sentence transformer.

        Args:
            query (UserQuery): The user query object.

        Returns:
            List[float]: The embedding vector as a list of floats.
        """
        query_text = query.get_user_query()
        query_embeddings = self.embedder.encode(query_text).tolist()
        return query_embeddings