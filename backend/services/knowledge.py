"""
Knowledge base retrieval module using Supabase PostgreSQL.

This module handles searching the medical knowledge base stored in Supabase
using full-text search and similarity matching.

Usage:
    from backend.services.knowledge import search_knowledge

    results = search_knowledge("headache and fever", limit=5)
"""

import logging
import re
from typing import Any, Dict, List, Optional, Union

from supabase import create_client

from backend.config import SUPABASE_KEY, SUPABASE_URL, CHUNK_MIN_WORDS, CHUNK_MAX_WORDS, CHUNK_OVERLAP_WORDS

logger = logging.getLogger(__name__)

_supabase_client = None


def _get_client():
    """Get or create the Supabase client."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Supabase credentials not configured")
        return None

    try:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return _supabase_client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        return None


def search_knowledge(query: str, limit: int = 5) -> List[Dict]:
    """
    Search the medical knowledge base for relevant documents.

    Uses keyword extraction and topic matching to find relevant content.

    Args:
        query: The search query (user's symptom text).
        limit: Maximum number of results to return.

    Returns:
        List of knowledge chunks with text, source, topic, and distance.
    """
    try:
        client = _get_client()
        if client is None:
            return []

        if not query or not query.strip():
            return []

        keywords = _extract_keywords(query.lower())

        if keywords:
            topics = ", ".join([f"'{k}'" for k in keywords])
            sql = f"""
                SELECT id, topic, source, content, chunk_index,
                       ts_rank(to_tsvector('english', content), plainto_tsquery('english', '{query}')) as rank
                FROM medical_knowledge
                WHERE topic IN ({topics})
                   OR source ILIKE '%{keywords[0]}%'
                   OR content ILIKE '%{keywords[0]}%'
                ORDER BY rank DESC
                LIMIT {limit};
            """
            try:
                response = client.rpc("search_knowledge", {"query_text": query, "limit_num": limit}).execute()
                if response.data:
                    return [
                        {
                            "text": r["content"],
                            "source": r["source"],
                            "topic": r["topic"],
                            "distance": 1.0 - (r.get("rank", 0) / 10),
                        }
                        for r in response.data
                    ]
            except Exception:
                pass

            try:
                response = client.table("medical_knowledge").select("*").limit(limit).execute()
                return [
                    {
                        "text": r["content"],
                        "source": r["source"],
                        "topic": r["topic"],
                        "distance": 0.5,
                    }
                    for r in response.data
                ]
            except Exception as e:
                logger.error(f"Failed to fetch knowledge: {e}")
                return []
        else:
            response = client.table("medical_knowledge").select("*").limit(limit).execute()
            return [
                {
                    "text": r["content"],
                    "source": r["source"],
                    "topic": r["topic"],
                    "distance": 0.5,
                }
                for r in response.data
            ]

    except Exception as e:
        logger.error(f"Knowledge search failed: {e}")
        return []


def _extract_keywords(text: str) -> List[str]:
    """Extract medical keywords from text."""
    medical_terms = {
        "headache": "headache",
        "fever": "fever",
        "cough": "cough",
        "rash": "rash",
        "nausea": "nausea",
        "vomit": "nausea",
        "dizziness": "dizziness",
        "dizzy": "dizziness",
        "pain": "pain",
        "chest": "chest pain",
        "breathing": "breathing",
        "shortness of breath": "breathing",
        "fatigue": "fatigue",
        "tired": "fatigue",
        "sore throat": "sore throat",
        "throat": "sore throat",
        "cold": "cold",
        "flu": "flu",
        "stomach": "stomach",
        "abdominal": "abdominal",
        "diarrhea": "diarrhea",
    }

    found = []
    text_lower = text.lower()
    for term, topic in medical_terms.items():
        if term in text_lower and topic not in found:
            found.append(topic)
    return found


def seed_knowledge_base(documents: List[Dict]) -> int:
    """
    Seed the knowledge base with medical documents.

    Args:
        documents: List of document dicts with source, topic, and content.

    Returns:
        Number of chunks inserted.
    """
    try:
        client = _get_client()
        if client is None:
            return 0

        total = 0
        for doc in documents:
            chunks = _chunk_text(doc["content"])
            for i, chunk in enumerate(chunks):
                data = {
                    "topic": doc["topic"],
                    "source": doc["source"],
                    "content": chunk,
                    "chunk_index": i,
                }
                client.table("medical_knowledge").insert(data).execute()
                total += 1

        return total
    except Exception as e:
        logger.error(f"Failed to seed knowledge base: {e}")
        return 0


def _chunk_text(text: str) -> List[str]:
    """Split text into chunks using config parameters."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks = []
    current_sentences = []
    current_word_count = 0
    overlap_sentences = []
    overlap_word_count = 0

    min_words = CHUNK_MIN_WORDS
    max_words = CHUNK_MAX_WORDS
    overlap_words = CHUNK_OVERLAP_WORDS

    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        current_sentences.append(sentence)
        current_word_count += sentence_word_count

        if current_word_count >= min_words:
            chunks.append(" ".join(current_sentences))

            overlap_text = []
            overlap_count = 0
            for s in reversed(current_sentences):
                swc = len(s.split())
                if overlap_count + swc > overlap_words:
                    break
                overlap_text.insert(0, s)
                overlap_count += swc
            current_sentences = list(overlap_text)
            current_word_count = overlap_count

    if current_sentences:
        remaining = " ".join(current_sentences)
        if len(remaining.split()) > 50:
            chunks.append(remaining)

    return chunks if chunks else [text]


def get_knowledge_count() -> int:
    """Get total count of knowledge chunks in the database."""
    try:
        client = _get_client()
        if client is None:
            return 0
        response = client.table("medical_knowledge").select("id", count="exact").execute()
        return response.count or 0
    except Exception as e:
        logger.error(f"Failed to get knowledge count: {e}")
        return 0