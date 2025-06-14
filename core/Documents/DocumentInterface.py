from abc import ABC, abstractmethod

class Document(ABC):

    @abstractmethod
    def get_document(self) -> list[str]:
        pass

    def get_filename(self) -> str:
        pass