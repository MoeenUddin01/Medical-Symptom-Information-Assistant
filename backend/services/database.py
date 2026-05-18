"""
Database integration module for logging queries and conditions to Supabase.

This module handles persisting symptom analysis results to a Supabase PostgreSQL
database for audit logging and analytics purposes.

Usage:
    from backend.services.database import log_query, get_recent_queries, get_query_by_id

    query_id = log_query("I have a headache", False, None, conditions)
    recent = get_recent_queries(limit=10)
    query = get_query_by_id(query_id)
"""

import logging
from typing import Any, Dict, List, Optional

from supabase import create_client

from backend.config import SUPABASE_KEY, SUPABASE_URL

logger = logging.getLogger(__name__)

_supabase_client = None


def _get_supabase_client():
    """
    Get or create the Supabase client instance.

    Returns:
        The configured Supabase client, or None if not configured.

    Raises:
        RuntimeError: If Supabase credentials are not configured.
    """
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.warning("Supabase credentials not configured. Database logging disabled.")
        return None

    try:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return _supabase_client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        return None


def log_query(
    symptom_text: str,
    is_emergency: bool,
    matched_keyword: Optional[str],
    conditions: List[Dict[str, Any]],
) -> Optional[str]:
    """
    Log a symptom query and its results to the database.

    Inserts a row into the queries table, then inserts a row into conditions_log
    for each condition returned. This enables audit logging and analytics.

    Args:
        symptom_text: The original user symptom description.
        is_emergency: Whether an emergency was detected.
        matched_keyword: The emergency keyword that was matched, if any.
        conditions: List of condition dicts with keys: name, explanation, severity, source.

    Returns:
        The new query ID as a string, or None if logging failed or Supabase is not configured.
    """
    try:
        client = _get_supabase_client()
        if client is None:
            return None

        raw_response = {"conditions": conditions}

        query_data = {
            "symptom_text": symptom_text,
            "is_emergency": is_emergency,
            "matched_keyword": matched_keyword,
            "conditions_count": len(conditions) if conditions else 0,
            "raw_response": raw_response,
        }

        query_response = client.table("queries").insert(query_data).execute()

        if not query_response.data or len(query_response.data) == 0:
            logger.error("Failed to insert query: no data returned")
            return None

        query_id = query_response.data[0].get("id")
        if not query_id:
            logger.error("Failed to get query ID from insert response")
            return None

        for condition in conditions:
            try:
                condition_data = {
                    "query_id": query_id,
                    "condition_name": str(condition.get("name", "")),
                    "severity": str(condition.get("severity", "moderate")),
                    "source": str(condition.get("source", "unknown")),
                }
                client.table("conditions_log").insert(condition_data).execute()
            except Exception as e:
                logger.warning(f"Failed to log condition '{condition.get('name')}': {str(e)}")
                continue

        return str(query_id)

    except Exception as e:
        logger.error(f"Failed to log query to database: {str(e)}")
        return None


def get_recent_queries(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch the most recent symptom queries from the database.

    Args:
        limit: Maximum number of queries to return (default: 10).

    Returns:
        List of query dicts ordered by created_at descending.
        Returns empty list on error or if Supabase is not configured.
    """
    try:
        client = _get_supabase_client()
        if client is None:
            return []

        if limit <= 0:
            limit = 10

        response = (
            client.table("queries")
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )

        return response.data if response.data else []

    except Exception as e:
        logger.error(f"Failed to fetch recent queries: {str(e)}")
        return []


def get_query_by_id(query_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a single query by its ID from the database.

    Args:
        query_id: The UUID of the query to fetch.

    Returns:
        The query dict if found, or None if not found or on error.
    """
    try:
        client = _get_supabase_client()
        if client is None:
            return None

        if not query_id or not query_id.strip():
            return None

        response = (
            client.table("queries")
            .select("*")
            .eq("id", query_id.strip())
            .execute()
        )

        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

    except Exception as e:
        logger.error(f"Failed to fetch query by ID: {str(e)}")
        return None