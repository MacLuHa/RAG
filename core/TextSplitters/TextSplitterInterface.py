from abc import ABC, abstractmethod
from Documents.DocumentInterface import Document

class TextSplitter(ABC):

    @abstractmethod
    def split_document(self, document: Document) -> list[str]:
        pass