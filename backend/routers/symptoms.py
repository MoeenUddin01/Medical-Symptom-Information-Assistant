"""
Symptoms API router for the Medical Symptom Information Assistant.

This module defines the POST /api/symptoms endpoint that orchestrates
the full symptom analysis pipeline: emergency detection, NER, retrieval,
and LLM response generation.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.services.emergency import check_emergency
from backend.services.llm import build_disclaimer, call_llm
from backend.services.ner import build_search_query, extract_medical_entities
from backend.services.retrieval import retrieve_chunks

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


router = APIRouter(prefix="/api")


@router.post("/symptoms", response_model=SymptomResponse)
@limiter.limit("20/minute")
async def analyze_symptoms(request: Request, symptom_request: SymptomRequest) -> SymptomResponse:
    """
    Analyze user-reported symptoms through the full processing pipeline.
    
    Executes the pipeline in strict order:
    1. Emergency keyword detection (returns immediately if emergency)
    2. Medical entity extraction via NER
    3. Search query construction
    4. Vector retrieval from ChromaDB
    5. LLM response generation with grounded medical context
    
    Args:
        request: SymptomRequest containing the user's symptom description.
        
    Returns:
        SymptomResponse with emergency status, conditions, and disclaimer.
    """
    try:
        user_input = symptom_request.text.strip()
        
        emergency_result = check_emergency(user_input)
        
        if emergency_result["is_emergency"]:
            return SymptomResponse(
                is_emergency=True,
                emergency_message=emergency_result["emergency_message"],
                conditions=[],
                disclaimer=build_disclaimer(),
            )
        
        entities = extract_medical_entities(user_input)
        
        search_query = build_search_query(entities, user_input)
        
        chunks = retrieve_chunks(search_query)
        
        conditions = call_llm(user_input, chunks)
        
        return SymptomResponse(
            is_emergency=False,
            emergency_message=None,
            conditions=conditions,
            disclaimer=build_disclaimer(),
        )
    
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your request. Please try again later.",
        )
