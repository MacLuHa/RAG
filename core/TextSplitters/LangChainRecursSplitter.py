from TextSplitters.TextSplitterInterface import TextSplitter
from Documents.DocumentInterface import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional, Any

class LangChainRecursSplitter(TextSplitter):
    """
    Text splitter that wraps LangChain's RecursiveCharacterTextSplitter.

    Splits a given document into chunks based on recursive separators
    and customizable parameters like chunk size and overlap. Useful for
    preparing documents for embedding or indexing.

    Attributes:
        text_splitter (RecursiveCharacterTextSplitter): LangChain's internal splitter instance.
    """
    def __init__(
            self, 
            chunk_size: int = 300,
            chunk_overlap: int = 40,
            length_function: Any = len,
            is_separator_regex: bool = True) -> None:
        """
        Initializes the recursive character text splitter.

        Args:
            chunk_size (int): Maximum number of characters per chunk.
            chunk_overlap (int): Number of overlapping characters between chunks.
            length_function (Callable): Function to calculate the length of text blocks.
            is_separator_regex (bool): Whether separators are treated as regular expressions.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            length_function = length_function,
            is_separator_regex = is_separator_regex,
            separators=["\n\n", "\n", " ", ""]
        )

    @staticmethod
    def _check_empty_list(list_: Optional[List[str]]) -> bool:
        """
        Checks if a list is None or empty.

        Args:
            list_ (Optional[List[str]]): The list to check.

        Returns:
            bool: True if the list is None or empty, False otherwise.
        """
        return (list_ is None) or (len(list_) == 0)

    def split_document(self, document: Document) -> List[str]:
        """
        Splits the document into text chunks using recursive character rules.

        Args:
            document (Document): A document object implementing `get_document()`,
                                 which returns a list of strings (pages or sections).

        Returns:
            List[str]: A list of text chunks.

        Raises:
            Exception: If the document has no content or pages.
        """     
        documents = document.get_document()
        if self._check_empty_list(documents):
            raise Exception("Document contains no pages or is empty")
        chunks = [doc.page_content for doc in self.text_splitter.create_documents(documents)]
        return chunks
    
if __name__ == '__main__':
    from Documents.PdfDocument import PdfDocument
    import numpy as np

    document = PdfDocument('../examples/Устав внутренней службы ВС РФ.pdf')
    text_splitter = LangChainRecursSplitter()
    chunks = text_splitter.split_document(document)
    print(chunks[np.random.randint(0, len(chunks))])