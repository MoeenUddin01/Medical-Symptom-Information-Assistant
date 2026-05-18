"""
Emergency detection module for the Medical Symptom Information Assistant.

This module MUST be called FIRST in the symptom processing pipeline,
BEFORE any other service (NER, retrieval, LLM). It performs keyword-based
detection of potentially life-threatening symptoms and returns immediately
without proceeding to further processing.

Usage:
    from backend.services.emergency import check_emergency
    
    result = check_emergency("I have severe chest pain")
    if result["is_emergency"]:
        # Show emergency UI, do not proceed to RAG pipeline
"""

from typing import Dict, List, Optional

from backend.config import EMERGENCY_KEYWORDS


def get_emergency_keywords() -> List[str]:
    """Return the full list of emergency keywords for detection."""
    return EMERGENCY_KEYWORDS.copy()


def check_emergency(text: str) -> Dict[str, Optional[str | bool]]:
    """
    Check if the input text contains any emergency keywords.
    
    This function must run BEFORE any other pipeline step. It performs
    a simple keyword match against the predefined emergency keywords list.
    
    Args:
        text: The user's symptom description input text.
        
    Returns:
        Dict with keys:
            - is_emergency: bool - True if emergency keyword found
            - matched_keyword: str or None - The keyword that matched
            - emergency_message: str or None - Warning message if emergency
    """
    # Lowercase the input text to perform case-insensitive matching
    text_lower = text.lower()
    
    # Iterate through all emergency keywords to find a match
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text_lower:
            # Emergency keyword detected - return emergency response
            return {
                "is_emergency": True,
                "matched_keyword": keyword,
                "emergency_message": (
                    "These symptoms may indicate a life-threatening emergency. "
                    "Call emergency services immediately (e.g. 115, 1122, 911). "
                    "Do not wait."
                ),
            }
    
    # No emergency keywords found - proceed with normal pipeline
    return {
        "is_emergency": False,
        "matched_keyword": None,
        "emergency_message": None,
    }