"""
Named Entity Recognition (NER) module for medical symptom extraction.

This module uses scispacy with the en_core_sci_sm model to extract
medical entities from user symptom descriptions. The extracted entities
are used to build optimized search queries for the vector retrieval step.

Usage:
    from backend.services.ner import extract_medical_entities, build_search_query
    
    entities = extract_medical_entities("I have a severe headache and chest pain")
    query = build_search_query(entities, "I have a severe headache and chest pain")
"""

from typing import Dict, List

import spacy


_nlp_model = None


def _get_model():
    """Load and return the scispacy model, loading once at module level."""
    global _nlp_model
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load("en_core_sci_sm")
        except OSError:
            raise RuntimeError(
                "scispacy model 'en_core_sci_sm' not found. "
                "Please install it with: python -m spacy download en_core_sci_sm"
            )
    return _nlp_model


def extract_medical_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract medical entities from the input text using scispacy.
    
    The function identifies symptoms, body parts, and medical conditions
    from the text and returns them categorized for downstream processing.
    
    Args:
        text: The user's symptom description text.
        
    Returns:
        Dict with keys:
            - symptoms: list of extracted symptom entities
            - body_parts: list of extracted body part entities
            - conditions: list of extracted condition/disease entities
            - all_entities: flat list of all unique entity strings
    """
    if not text or not text.strip():
        return {
            "symptoms": [],
            "body_parts": [],
            "conditions": [],
            "all_entities": [],
        }
    
    nlp = _get_model()
    doc = nlp(text.strip())
    
    symptoms = []
    body_parts = []
    conditions = []
    seen = set()
    
    for ent in doc.ents:
        label = ent.label_
        text_clean = ent.text.strip().lower()
        if text_clean in seen:
            continue
        seen.add(text_clean)
        
        if label in ["SYMPTOM", "SIGN_SYMPTOM"]:
            symptoms.append(ent.text.strip())
        elif label in ["ANATOMY", "BODY_PART"]:
            body_parts.append(ent.text.strip())
        elif label in ["DISORDER", "DISEASE", "CANCER"]:
            conditions.append(ent.text.strip())
    
    all_entities = list(set(symptoms + body_parts + conditions))
    
    return {
        "symptoms": symptoms,
        "body_parts": body_parts,
        "conditions": conditions,
        "all_entities": all_entities,
    }


def build_search_query(entities: Dict[str, List[str]], original_text: str) -> str:
    """
    Build an optimized search query for vector retrieval.
    
    Combines the top 5 extracted entities with the original text
    to create a rich search string for ChromaDB retrieval.
    
    Args:
        entities: Dict of extracted entities from extract_medical_entities.
        original_text: The original user input text.
        
    Returns:
        A combined search string for vector retrieval.
    """
    all_entities = entities.get("all_entities", [])
    top_entities = all_entities[:5]
    
    if not top_entities:
        return original_text
    
    entity_string = " ".join(top_entities)
    combined = f"{original_text} {entity_string}"
    
    return combined.strip()