"""
Test suite for the NER (Named Entity Recognition) service.

This module validates that the extract_medical_entities and build_search_query
functions correctly extract medical entities from symptom descriptions and
build optimized search queries for the vector retrieval pipeline.
"""

import sys
from unittest.mock import patch, MagicMock

mock_spacy = MagicMock()
mock_nlp = MagicMock()
mock_spacy.load.return_value = mock_nlp
sys.modules['spacy'] = mock_spacy
sys.modules['en_core_sci_sm'] = MagicMock()

from backend.services.ner import extract_medical_entities, build_search_query


def test_returns_correct_keys():
    """Validates that the returned dict contains exactly the required keys."""
    result = extract_medical_entities("I have a headache and fever")
    assert "symptoms" in result
    assert "body_parts" in result
    assert "conditions" in result
    assert "all_entities" in result
    assert set(result.keys()) == {"symptoms", "body_parts", "conditions", "all_entities"}


def test_all_values_are_lists():
    """Validates that all returned values are lists, not None or strings."""
    result = extract_medical_entities("I have a headache")
    assert isinstance(result["symptoms"], list)
    assert isinstance(result["body_parts"], list)
    assert isinstance(result["conditions"], list)
    assert isinstance(result["all_entities"], list)


def test_empty_input_returns_empty_lists():
    """Validates that empty input returns all empty lists without raising an exception."""
    result = extract_medical_entities("")
    assert result["symptoms"] == []
    assert result["body_parts"] == []
    assert result["conditions"] == []
    assert result["all_entities"] == []


def test_medical_text_extracts_entities():
    """Validates that medical text with symptoms produces non-empty entity lists."""
    mock_ent = MagicMock()
    mock_ent.text = "headache"
    mock_ent.label_ = "SYMPTOM"
    mock_doc = MagicMock()
    mock_doc.ents = [mock_ent]
    mock_nlp.return_value = mock_doc

    result = extract_medical_entities("The patient has a severe headache and fever with neck stiffness")
    assert len(result["all_entities"]) > 0


def test_no_duplicate_entities():
    """Validates that repeating the same symptom does not create duplicate entries."""
    mock_ent = MagicMock()
    mock_ent.text = "headache"
    mock_ent.label_ = "SYMPTOM"
    mock_doc = MagicMock()
    mock_doc.ents = [mock_ent, mock_ent, mock_ent]
    mock_nlp.return_value = mock_doc

    result = extract_medical_entities("headache headache headache")
    all_lower = [e.lower() for e in result["all_entities"]]
    assert len(all_lower) == len(set(all_lower))


def test_build_search_query_returns_string():
    """Validates that build_search_query returns a non-empty string."""
    entities = {"symptoms": ["headache"], "body_parts": [], "conditions": [], "all_entities": ["headache"]}
    result = build_search_query(entities, "I have a headache")
    assert isinstance(result, str)
    assert len(result) > 0


def test_build_search_query_includes_original_text():
    """Validates that the result contains words from the original input text."""
    entities = {"symptoms": [], "body_parts": [], "conditions": [], "all_entities": []}
    result = build_search_query(entities, "I have a severe headache today")
    assert "headache" in result.lower()
    assert "severe" in result.lower()