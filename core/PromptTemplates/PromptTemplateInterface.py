from abc import ABC, abstractmethod
from Queries.UserQueryInterface import UserQuery

class PromptTemplate(ABC):

    @abstractmethod
    def get_prompt(self) -> str:
        pass