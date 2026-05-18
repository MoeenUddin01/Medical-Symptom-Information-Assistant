"""
Test suite for the emergency detection service.

This module validates that the check_emergency function correctly identifies
potentially life-threatening symptoms based on predefined emergency keywords.
All tests ensure the system can detect emergencies before proceeding with
the RAG pipeline.
"""

import pytest

from backend.services.emergency import check_emergency, get_emergency_keywords
from backend.config import EMERGENCY_KEYWORDS


def test_exact_keyword_match():
    """Validates that a direct emergency keyword triggers an emergency response."""
    result = check_emergency("I have chest pain")
    assert result["is_emergency"] is True
    assert result["matched_keyword"] == "chest pain"


def test_case_insensitive_match():
    """Validates that keyword detection is case-insensitive."""
    result = check_emergency("I have CHEST PAIN right now")
    assert result["is_emergency"] is True
    assert result["matched_keyword"] == "chest pain"


def test_partial_sentence_match():
    """Validates that keywords embedded within sentences are detected."""
    result = check_emergency("since yesterday I have had difficulty breathing and feel dizzy")
    assert result["is_emergency"] is True
    assert result["matched_keyword"] == "difficulty breathing"


def test_no_emergency_keywords():
    """Validates that non-emergency symptoms return no emergency flag."""
    result = check_emergency("I have a mild headache and runny nose")
    assert result["is_emergency"] is False
    assert result["matched_keyword"] is None


def test_empty_string():
    """Validates that empty input does not raise an exception and returns non-emergency."""
    result = check_emergency("")
    assert result["is_emergency"] is False
    assert result["matched_keyword"] is None


def test_all_keywords_detected():
    """Validates that every keyword in the EMERGENCY_KEYWORDS list triggers detection."""
    keywords = get_emergency_keywords()
    for keyword in keywords:
        result = check_emergency(keyword)
        assert result["is_emergency"] is True, f"Keyword '{keyword}' should trigger emergency"


def test_emergency_message_content():
    """Validates that the emergency message contains required urgent language."""
    result = check_emergency("chest pain")
    assert result["is_emergency"] is True
    assert result["emergency_message"] is not None
    assert "emergency" in result["emergency_message"].lower()
    assert "immediately" in result["emergency_message"].lower()