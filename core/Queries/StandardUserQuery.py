from Queries.UserQueryInterface import UserQuery

class StandardUserQuery(UserQuery):
    """
    A standard implementation of the UserQuery interface that stores and returns a user-provided query string.
    """
    def __init__(self, query: str) -> None:
        """
        Initializes a user query object.

        Args:
            query (str): The user input query as a plain string.
        """
        self._user_query: str = query

    def get_user_query(self) -> str:
        """
        Returns:
            str: The stored user query.
        """
        return self._user_query
        