import pytest
import os
from dotenv import load_dotenv
from together import Together

from rag.embedder import Embedder

load_dotenv()

API_KEY = os.getenv('API_KEY_LLM', None)
MODEL_EMBEDDER = 'togethercomputer/m2-bert-80M-8k-retrieval'

if API_KEY is None:
    raise Exception("Api key not set")

@pytest.fixture
def client_together():
    client_together = Together(
        api_key=API_KEY
        )
    return client_together


def test_embedding(client_together):
    response = client_together.embeddings.create(
    model = MODEL_EMBEDDER,
    input = "Our solar system orbits the Milky Way galaxy at about 515,000 mph"
    )

    assert response.model == MODEL_EMBEDDER
    assert response.object =='list'
    assert isinstance(response.data[0].embedding, list)