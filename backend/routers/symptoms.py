"""
Symptoms API router for the Medical Symptom Information Assistant.

This module defines the POST /api/symptoms endpoint that orchestrates
the full symptom analysis pipeline: emergency detection, NER (if available),
knowledge retrieval, LLM response generation, and query logging to Supabase.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.services.database import get_query_by_id, get_recent_queries, log_query
from backend.services.emergency import check_emergency
from backend.services.llm import build_disclaimer, call_llm
from backend.services.retrieval import format_chunks_for_prompt, retrieve_chunks

logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)


class SymptomRequest(BaseModel):
    """Request model for symptom analysis."""

    text: str = Field(..., min_length=3, max_length=1000)


class SymptomResponse(BaseModel):
    """Response model for symptom analysis results."""

    is_emergency: bool
    emergency_message: Optional[str] = None
    conditions: List[dict]
    disclaimer: str


class QueryHistoryItem(BaseModel):
    """Response model for a single query in history."""

    id: str
    created_at: str
    symptom_text: str
    is_emergency: bool
    matched_keyword: Optional[str] = None
    conditions_count: int


class QueryHistoryDetailResponse(BaseModel):
    """Response model for detailed query history with conditions."""

    id: str
    created_at: str
    symptom_text: str
    is_emergency: bool
    matched_keyword: Optional[str] = None
    conditions_count: int
    conditions: List[dict]


router = APIRouter(prefix="/api")


def _extract_keywords_from_text(text: str) -> str:
    """Simple keyword extraction from text."""
    keywords = []
    text_lower = text.lower()

    medical_terms = {
        "headache": "headache",
        "migraine": "headache",
        "fever": "fever",
        "temperature": "fever",
        "cough": "cough",
        "coughing": "cough",
        "rash": "rash",
        "skin": "rash",
        "nausea": "nausea",
        "vomiting": "nausea",
        "vomit": "nausea",
        "dizziness": "dizziness",
        "dizzy": "dizziness",
        "vertigo": "dizziness",
        "breathing": "breathing",
        "shortness of breath": "breathing",
        "chest pain": "chest pain",
        "abdominal": "abdominal",
        "stomach": "abdominal",
        "diarrhea": "diarrhea",
        "fatigue": "fatigue",
        "tired": "fatigue",
    }

    for term, topic in medical_terms.items():
        if term in text_lower:
            keywords.append(topic)

    return " ".join(keywords) if keywords else text


@router.post("/symptoms", response_model=SymptomResponse)
@limiter.limit("20/minute")
async def analyze_symptoms(request: Request, symptom_request: SymptomRequest) -> SymptomResponse:
    """
    Analyze user-reported symptoms through the processing pipeline.

    Pipeline steps:
    1. Emergency keyword detection (returns immediately if emergency)
    2. Knowledge base retrieval from Supabase
    3. LLM response generation with grounded medical context
    4. Query logging to Supabase (non-blocking)

    Args:
        request: SymptomRequest containing the user's symptom description.

    Returns:
        SymptomResponse with emergency status, conditions, and disclaimer.
    """
    user_input = symptom_request.text.strip()
    emergency_result = check_emergency(user_input)

    if emergency_result["is_emergency"]:
        result = SymptomResponse(
            is_emergency=True,
            emergency_message=emergency_result["emergency_message"],
            conditions=[],
            disclaimer=build_disclaimer(),
        )

        try:
            log_query(
                symptom_text=user_input,
                is_emergency=True,
                matched_keyword=emergency_result.get("matched_keyword"),
                conditions=[],
            )
        except Exception as e:
            logger.warning(f"Failed to log emergency query: {str(e)}")

        return result

    try:
        search_query = _extract_keywords_from_text(user_input)
        if not search_query.strip():
            search_query = user_input

        chunks = retrieve_chunks(search_query)

        if not chunks:
            chunks = [{"text": "No specific medical information found for these symptoms. Please consult a healthcare professional.", "source": "System", "topic": "general", "distance": 1.0}]

        conditions = call_llm(user_input, chunks)

        result = SymptomResponse(
            is_emergency=False,
            emergency_message=None,
            conditions=conditions,
            disclaimer=build_disclaimer(),
        )

        try:
            log_query(
                symptom_text=user_input,
                is_emergency=False,
                matched_keyword=None,
                conditions=conditions,
            )
        except Exception as e:
            logger.warning(f"Failed to log query: {str(e)}")

        return result

    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your request. Please try again later.",
        )


@router.get("/history", response_model=List[QueryHistoryItem])
async def get_history(limit: int = 10) -> List[QueryHistoryItem]:
    """
    Get the most recent symptom queries.

    Args:
        limit: Maximum number of queries to return (default: 10, max: 100).

    Returns:
        List of recent queries ordered by created_at descending.
    """
    if limit <= 0:
        limit = 10
    if limit > 100:
        limit = 100

    queries = get_recent_queries(limit=limit)

    return [
        QueryHistoryItem(
            id=q.get("id", ""),
            created_at=str(q.get("created_at", "")),
            symptom_text=q.get("symptom_text", ""),
            is_emergency=q.get("is_emergency", False),
            matched_keyword=q.get("matched_keyword"),
            conditions_count=q.get("conditions_count", 0),
        )
        for q in queries
    ]


@router.get("/history/{query_id}", response_model=QueryHistoryDetailResponse)
async def get_query_detail(query_id: str) -> QueryHistoryDetailResponse:
    """
    Get details of a specific query by ID, including logged conditions.

    Args:
        query_id: The UUID of the query to fetch.

    Returns:
        The query details with matched conditions.

    Raises:
        HTTPException: 404 if query not found.
    """
    query = get_query_by_id(query_id)

    if query is None:
        raise HTTPException(
            status_code=404,
            detail=f"Query with ID '{query_id}' not found.",
        )

    raw = query.get("raw_response", {})
    conditions = []
    if isinstance(raw, dict):
        conditions = raw.get("conditions", [])
    elif isinstance(raw, str):
        import json
        try:
            parsed = json.loads(raw)
            conditions = parsed.get("conditions", [])
        except Exception:
            pass

    return QueryHistoryDetailResponse(
        id=query.get("id", ""),
        created_at=str(query.get("created_at", "")),
        symptom_text=query.get("symptom_text", ""),
        is_emergency=query.get("is_emergency", False),
        matched_keyword=query.get("matched_keyword"),
        conditions_count=query.get("conditions_count", 0),
        conditions=conditions,
    )