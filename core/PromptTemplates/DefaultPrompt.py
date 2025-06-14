from PromptTemplateInterface import PromptTemplate
from Queries.UserQueryInterface import UserQuery
from typing import List

class DefaultPrompt(PromptTemplate):
    """
    Default prompt builder for an LLM query based on user input and relevant context.
    """
    def __init__(self, user_query: UserQuery, context: List[str]) -> None:
        """
        Args:
            user_query (UserQuery): The user's query object.
            context (List[str]): List of relevant text chunks (e.g. from retrieval).
        """
        self.prompt = f"""
        Based on the following context, answer the user's query.

        ### Context:
        {"\n\n\n".join(context)}

        ### Query: {user_query.get_user_query}

        ### Answer:
        """
        
    def get_prompt(self) -> str:
        """Returns the generated prompt string."""
        return self.prompt
    
