from abc import ABC, abstractmethod

from PromptTemplates.PromptTemplateInterface import PromptTemplate

class Generator(ABC):

    @abstractmethod
    def generate_response(self, prompt: PromptTemplate) -> str:
        pass