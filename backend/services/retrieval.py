"""
Knowledge retrieval module using Supabase PostgreSQL.

This module handles querying the Supabase medical knowledge base
to retrieve relevant document chunks based on the user's symptom query.

Usage:
    from backend.services.retrieval import retrieve_chunks, format_chunks_for_prompt

    chunks = retrieve_chunks("I have a severe headache")
    context = format_chunks_for_prompt(chunks)
"""

from typing import Dict, List

from backend.services.knowledge import search_knowledge, get_knowledge_count


def retrieve_chunks(query: str, n_results: int = 5) -> List[Dict[str, str | float]]:
    """
    Retrieve relevant medical document chunks for a given query.

    Uses Supabase full-text search to find relevant medical content
    based on symptom keywords and topic matching.

    Args:
        query: The search query string (user's symptom description).
        n_results: Maximum number of chunks to retrieve (default: 5).

    Returns:
        List of dicts, each containing:
            - text: the chunk content
            - source: the source document name
            - topic: the medical topic category
            - distance: the similarity score (lower is more similar)
    """
    count = get_knowledge_count()
    if count == 0:
        return []

    chunks = search_knowledge(query, limit=n_results)
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