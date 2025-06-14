from VectorDBs.VectordbInterface import VectorDB
from Documents.DocumentInterface import Document
from TextSplitters.TextSplitterInterface import TextSplitter
from typing import List, Dict, Any
from chromadb import PersistentClient

import chromadb
import os
from datetime import datetime

class ChromaDB(VectorDB):
    """
    A vector database implementation using ChromaDB for document storage and retrieval.

    This class allows adding parsed documents into a persistent ChromaDB collection
    and querying them using vector embeddings. Intended for use in retrieval-augmented
    generation (RAG) pipelines.

    Attributes:
        text_splitter (TextSplitter): A text splitter instance used to chunk documents before storage.
        collection_name (str): The name of the collection inside the ChromaDB store.
        _path_db (str): Full path to the ChromaDB storage file.
        client (chromadb.PersistentClient): Persistent ChromaDB client instance.
        collection (chromadb.Collection): Collection used to store vectorized chunks.
    """
    def __init__(
            self,
            text_splitter: TextSplitter,
            vector_dir: str = '.db',
            filename_db: str = 'chroma.db',
            collection_name: str = 'docs',
            ) -> None:
        """
        Initializes the ChromaDB vector store and sets up a document collection.

        Args:
            text_splitter (TextSplitter): The text splitter to process documents before storage.
            vector_dir (str): Directory where the ChromaDB database will be stored.
            filename_db (str): Filename of the ChromaDB database.
            collection_name (str): Name of the document collection within ChromaDB.
        """
        self.text_splitter = text_splitter
        self.collection_name = collection_name
        self._path_db = os.path.join(vector_dir, filename_db)
        os.makedirs(vector_dir, exist_ok=True)

        self.client = chromadb.PersistentClient(self._path_db)
        self.collection = self.client.get_or_create_collection(
            name = self.collection_name,
            metadata = {
                "description": "collection of documents for RAG",
                "created": str(datetime.now())
            } )
    
    def _ping_db(self) -> bool:
        """
        Checks if the vector database file exists.

        Returns:
            bool: True if the database file exists, False otherwise.
        """
        return os.path.exists(self._path_db)
    
    def _delete_collection(self) -> None:
        """
        Deletes the collection from the ChromaDB client.
        Intended for internal use only (e.g. for testing or reset).
        """
        self.client.delete_collection(name=self.collection_name)

    def add_to_collection(self, document: Document) -> None:
        """
        Adds a document to the ChromaDB collection after splitting it into chunks.

        Each chunk is assigned a unique ID based on the document's filename and its order,
        and associated with metadata for traceability.

        Args:
            document (Document): A document object that provides:
                - get_document() -> List[str]: Returns the document content (e.g., pages).
                - get_filename() -> str: Returns the source filename.

        Raises:
            RuntimeError: If the ChromaDB database file is not found on disk.
        """
        filename = document.get_filename()
        if not self._ping_db():
            raise RuntimeError(f"Vector database {self._path_db} does not exist")

        chunks = self.text_splitter.split_document(document=document)
    
        self.collection.upsert(
            documents=chunks,
            ids = [f"{filename}_p{i}" for i in range(1, len(chunks) + 1)],
            metadatas= [{'source': filename, 'page': i} for i in range(1, len(chunks) + 1)]
        )

    def get_query_to_collection(self, embeddings: List[float], top_k: int = 5) -> Dict[str, List[Any]]:
        """
        Queries the vector database using given embedding and retrieves the most relevant chunks.

        Args:
            embeddings (List[float]): The embedding vector representing a user query.
            top_k (int): Number of top results to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing matched documents and their metadata.
        """
        retrieved_information = self.collection.query(
            query_embeddings=[embeddings],
            n_results=top_k,
            include=['documents', 'metadatas']
        )
        retrieved_docs = retrieved_information.get('documents', [[]])

        return retrieved_docs
    
if __name__ == '__main__':
    from Documents.PdfDocument import PdfDocument
    from Queries.StandardUserQuery import StandardUserQuery
    from Embedders.SentenceTransformerEmbedder import SentenceTransformerEmbedder
    from TextSplitters.LangChainRecursSplitter import LangChainRecursSplitter

    document = PdfDocument('../examples/Устав внутренней службы ВС РФ.pdf')
    user_query = StandardUserQuery("Каковы обязанности начальника гарнизона?")
    embedder = SentenceTransformerEmbedder()
    embeddings_query = embedder.create_embeddings(user_query)
    text_splitter = LangChainRecursSplitter()
    vector_db = ChromaDB(
        text_splitter=text_splitter,
    )
    vector_db.add_to_collection(document)
    result = vector_db.get_query_to_collection(embeddings_query)
    print(result)
    