from abc import ABC, abstractmethod
from typing import Union, List
import numpy as np

class BaseEmbedder(ABC):

    @abstractmethod
    def create_embeddings(self, inputs: Union[List[str], str]) -> List[List[float]]:
        pass

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 1, index: np.ndarray = None) -> List[int]:
        pass