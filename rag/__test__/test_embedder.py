import pytest
import sys 
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from rag.embedder import Embedder

@pytest.fixture
def embedder():
    embedder = Embedder()
    return embedder


def test_create_embeddings_one(embedder):
    response = embedder.create_embeddings(
        ['test text']
        )

    assert isinstance(response, list)
    assert len(response) == 1
    assert all(isinstance(element, float) for data in response for element in data)

def test_create_embeddings_more(embedder):
    response = embedder.create_embeddings(
        ['test text',
        'test text1',
        'test text2']
        )
    assert isinstance(response, list)
    assert len(response) == 3
    assert all(isinstance(element, float) for data in response for element in data)

def test_create_embeddings_empty_data(embedder):
    with pytest.raises(ValueError):
        response = embedder.create_embeddings(
        )