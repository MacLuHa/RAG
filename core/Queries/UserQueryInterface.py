from abc import ABC, abstractmethod

class UserQuery(ABC):

    @abstractmethod
    def get_user_query(self) -> str:
        pass