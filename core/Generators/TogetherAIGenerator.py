from Generators.GeneratorInterface import Generator
from utils.check_api_key import check_env_api_key
from dotenv import load_dotenv
from langchain_together import ChatTogether
from PromptTemplates.PromptTemplateInterface import PromptTemplate


load_dotenv()
check_env_api_key()

class TogetherAIGenerator(Generator):
    """
    A text generator using Together AI through Langchain's ChatTogether model.

    This class wraps the ChatTogether model to generate responses based on user input.
    """
    def __init__(
            self,
            api_key: str,
            model: str = 'meta-llama/Llama-3-70b-chat-hf',
            temperature: float = 0.7,
            max_tokens: int = 250
            ) -> None:
        """
        Initializes the TogetherAIGenerator with model configuration and API key.

        Args:
            api_key (str): API key for accessing Together AI services.
            model (str): The model name to use for generation.
            temperature (float): Controls randomness in output; higher values = more randomness.
            max_tokens (int): Maximum number of tokens to generate in the response.
        """
        self.model = model
        self.__api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.llm = ChatTogether(
            together_api_key = self.__api_key,
            model = self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
            )

    def generate_response(self, prompt: PromptTemplate) -> str:
        """
        Generates a response based on the given user query.

        Args:
            prompt (PromptTemplate): An object representing the user's input query.

        Returns:
            str: The generated text response from the language model.
        """
        response = self.llm.invoke(prompt)
        return response