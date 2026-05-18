"""
Test suite for the vector retrieval service.

This module validates that the retrieve_chunks and format_chunks_for_prompt
functions correctly query the ChromaDB vector store and format results
for the LLM prompt. External dependencies (ChromaDB, sentence-transformers)
are mocked to allow tests to run without a real database or model.
"""

import sys
import pytest
from unittest.mock import patch, MagicMock

fake_chunks_data = [
    {
        "documents": [["Headache is a common symptom..."]],
        "metadatas": [[{"source": "WHO Headache Fact Sheet", "topic": "headache"}]],
        "distances": [[0.15]],
    },
    {
        "documents": [["Fever often accompanies headaches..."]],
        "metadatas": [[{"source": "NHS Fever Guide", "topic": "fever"}]],
        "distances": [[0.22]],
    },
    {
        "documents": [["Tension headaches are caused by muscle strain..."]],
        "metadatas": [[{"source": "WHO Headache Fact Sheet", "topic": "headache"}]],
        "distances": [[0.28]],
    },
]

mock_collection = MagicMock()
mock_collection.count.return_value = 3
mock_collection.query.side_effect = lambda **kwargs: fake_chunks_data[0] if kwargs.get("n_results") == 1 else fake_chunks_data[0]

mock_chroma_client = MagicMock()
mock_chroma_client.get_or_create_collection.return_value = mock_collection

sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.config'] = MagicMock()
sys.modules['chromadb.config'].Settings = MagicMock
sys.modules['chromadb'].PersistentClient.return_value = mock_chroma_client
sys.modules['sentence_transformers'] = MagicMock()

from backend.services.retrieval import retrieve_chunks, format_chunks_for_prompt


@pytest.fixture
def reset_module_state():
    """Resets module-level cached clients between tests to ensure test isolation."""
    import backend.services.retrieval as retrieval_module
    retrieval_module._chroma_client = None
    retrieval_module._collection = None
    retrieval_module._embedding_model = None
    yield
    retrieval_module._chroma_client = None
    retrieval_module._collection = None
    retrieval_module._embedding_model = None


def test_returns_list_of_dicts(reset_module_state):
    """Validates that retrieve_chunks returns a list of dicts with required keys."""
    chunks = retrieve_chunks("headache and fever")
    assert isinstance(chunks, list)
    assert len(chunks) >= 1
    for chunk in chunks:
        assert "text" in chunk
        assert "source" in chunk
        assert "topic" in chunk
        assert "distance" in chunk


def test_respects_n_results_param(reset_module_state):
    """Validates that the n_results parameter is passed to ChromaDB query correctly."""
    with patch("backend.services.retrieval._get_chroma_collection") as mock_get_coll:
        fresh_mock = MagicMock()
        fresh_mock.count.return_value = 1
        fresh_mock.query.return_value = fake_chunks_data[0]
        mock_get_coll.return_value = fresh_mock
        with patch("backend.services.retrieval._get_embedding_model") as mock_model:
            mock_model.return_value.encode.return_value.tolist.return_value = [[0.1, 0.2]]
            retrieve_chunks("test query", n_results=10)
            fresh_mock.query.assert_called_with(query_embeddings=[[0.1, 0.2]], n_results=10)


def test_empty_results_returns_empty_list(reset_module_state):
    """Validates that empty ChromaDB results return an empty list without raising an exception."""
    with patch("backend.services.retrieval._get_chroma_collection") as mock_get_coll:
        empty_mock = MagicMock()
        empty_mock.count.return_value = 1
        empty_mock.query.return_value = {"documents": [[]], "metadatas": [[]], "distances": [[]]}
        mock_get_coll.return_value = empty_mock
        result = retrieve_chunks("nonexistent symptom xyz123")
        assert result == []


def test_missing_collection_raises_runtime_error(reset_module_state):
    """Validates that a missing collection raises RuntimeError with an 'ingest' hint in the message."""
    with patch("backend.services.retrieval._get_chroma_collection") as mock_get_coll:
        empty_mock = MagicMock()
        empty_mock.count.return_value = 0
        mock_get_coll.return_value = empty_mock
        with pytest.raises(RuntimeError) as exc_info:
            retrieve_chunks("any symptom")
        assert "ingest" in str(exc_info.value).lower()


def test_format_chunks_returns_string():
    """Validates that format_chunks_for_prompt returns a non-empty string for valid input."""
    chunks = [
        {"text": "Headache is a common condition.", "source": "WHO", "topic": "headache", "distance": 0.15},
        {"text": "Fever often accompanies illness.", "source": "NHS", "topic": "fever", "distance": 0.22},
        {"text": "Rest and hydration help recovery.", "source": "CDC", "topic": "general", "distance": 0.30},
    ]
    result = format_chunks_for_prompt(chunks)
    assert isinstance(result, str)
    assert len(result) > 0


def test_format_chunks_includes_source_names():
    """Validates that each source name from input chunks appears in the formatted output."""
    chunks = [
        {"text": "Headache text here.", "source": "WHO Headache Fact Sheet", "topic": "headache", "distance": 0.15},
        {"text": "Fever text here.", "source": "NHS Fever Guide", "topic": "fever", "distance": 0.22},
    ]
    result = format_chunks_for_prompt(chunks)
    assert "WHO Headache Fact Sheet" in result
    assert "NHS Fever Guide" in result