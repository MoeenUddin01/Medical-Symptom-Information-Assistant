"""
Vector retrieval module for medical symptom information.

This module handles querying the ChromaDB vector store to retrieve
relevant medical document chunks based on the user's symptom query.
The retrieved chunks are used as context for the LLM prompt.

Usage:
    from backend.services.retrieval import retrieve_chunks, format_chunks_for_prompt
    
    chunks = retrieve_chunks("I have a severe headache")
    context = format_chunks_for_prompt(chunks)
"""

from typing import Dict, List

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from backend.config import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, EMBEDDING_MODEL


_chroma_client = None
_collection = None
_embedding_model = None


def _get_chroma_collection():
    """Load and return the ChromaDB collection, initializing once at module level."""
    global _chroma_client, _collection
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False),
        )
    if _collection is None:
        _collection = _chroma_client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def _get_embedding_model():
    """Load and return the sentence-transformers model, initializing once at module level."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embedding_model


def retrieve_chunks(query: str, n_results: int = 5) -> List[Dict[str, str | float]]:
    """
    Retrieve the most similar document chunks from ChromaDB for a given query.
    
    This function embeds the query using sentence-transformers and performs
    a cosine similarity search against the stored medical document chunks.
    
    Args:
        query: The search query string (typically the user's symptom description
               combined with extracted entities).
        n_results: Maximum number of similar chunks to retrieve (default: 5).
        
    Returns:
        List of dicts, each containing:
            - text: the chunk content
            - source: the source document name
            - topic: the medical topic category
            - distance: the similarity score (lower is more similar)
            
    Raises:
        RuntimeError: If the ChromaDB collection does not exist or is empty,
                      indicating the ingestion pipeline has not been run.
    """
    if not query or not query.strip():
        return []
    
    collection = _get_chroma_collection()
    
    if collection.count() == 0:
        raise RuntimeError(
            "ChromaDB collection is empty. "
            "Please run the ingestion pipeline first: python -m backend.ingestion.ingest"
        )
    
    model = _get_embedding_model()
    query_embedding = model.encode([query.strip()]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )
    
    chunks = []
    if not results or not results.get("documents") or not results["documents"][0]:
        return []
    
    documents = results["documents"][0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    
    for i, doc in enumerate(documents):
        chunks.append({
            "text": doc,
            "source": metadatas[i].get("source", "unknown") if metadatas else "unknown",
            "topic": metadatas[i].get("topic", "unknown") if metadatas else "unknown",
            "distance": distances[i] if distances else 0.0,
        })
    
    return chunks


def format_chunks_for_prompt(chunks: List[Dict[str, str | float]]) -> str:
    """
    Format retrieved chunks into a clean string for the LLM prompt.
    
    Each chunk is numbered and includes its source document name.
    The formatted string is ready to be inserted into the LLM context.
    
    Args:
        chunks: List of chunk dicts from retrieve_chunks.
        
    Returns:
        A formatted string containing all chunks with source attribution.
        Returns empty string if chunks list is empty.
    """
    if not chunks:
        return ""
    
    formatted_parts = []
    for i, chunk in enumerate(chunks, start=1):
        text = chunk.get("text", "").strip()
        source = chunk.get("source", "Unknown").strip()
        if text:
            formatted_parts.append(f"[{i}] Source: {source}\n{text}")
    
    return "\n\n".join(formatted_parts)