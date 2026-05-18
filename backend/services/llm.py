"""
LLM integration module for the Medical Symptom Information Assistant.

This module handles calling the Claude API with the retrieved medical context
to generate symptom information responses.

Usage:
    from backend.services.llm import call_llm, build_disclaimer
    
    conditions = call_llm("I have a severe headache", chunks)
    disclaimer = build_disclaimer()
"""

import json
from typing import Dict, List

import anthropic
from anthropic import Anthropic

from backend.config import CLAUDE_API_KEY, CLAUDE_MODEL
from backend.services.retrieval import format_chunks_for_prompt


SYSTEM_PROMPT_TEMPLATE = """You are a medical information assistant. Your only job is to help users understand
their symptoms using the medical reference documents provided to you as context.

STRICT RULES:
1. Only use information present in the retrieved context below. Never add medical
   facts from your general knowledge.
2. For each possible condition, provide: name, plain-language explanation (2-3 sentences),
   severity level (mild/moderate/urgent), and the source document name.
3. If the context does not contain enough information to answer, say:
   "I could not find specific information about these symptoms in my reference documents.
   Please consult a healthcare professional."
4. Never diagnose. Always frame as "possible conditions" not "you have X".
5. Always end your response reminding the user to seek professional medical advice.

Respond ONLY in valid JSON matching this schema:
{{"conditions": [{{"name": str, "explanation": str, "severity": "mild"|"moderate"|"urgent", "source": str}}]}}

CONTEXT:
{{retrieved_chunks}}

USER SYMPTOMS:
{{user_input}}"""


def build_disclaimer() -> str:
    """
    Return the standard medical disclaimer for user-facing messages.
    
    Returns:
        The exact disclaimer string warning users to consult healthcare professionals.
    """
    return (
        "This tool is for information only and does not replace a doctor. "
        "Always consult a qualified healthcare professional for medical advice."
    )


def call_llm(user_input: str, chunks: List[Dict[str, str | float]]) -> List[Dict[str, str]]:
    """
    Call the Claude API with the user's symptoms and retrieved context.
    
    This function builds a prompt using the exact template from CLAUDE.md,
    sends it to Claude, and parses the JSON response into condition dictionaries.
    
    Args:
        user_input: The original user symptom description.
        chunks: List of retrieved document chunks from the retrieval service.
        
    Returns:
        List of condition dicts with keys: name, explanation, severity, source.
        On any error, returns a single condition dict with name "Parse Error"
        containing the raw model output or error message.
    """
    if not user_input or not user_input.strip():
        return [{"name": "Parse Error", "explanation": "No user input provided.", "severity": "moderate", "source": "system"}]
    
    if not chunks:
        return [{"name": "Parse Error", "explanation": "No relevant medical information found.", "severity": "moderate", "source": "system"}]
    
    try:
        if not CLAUDE_API_KEY:
            return [{"name": "Parse Error", "explanation": "Claude API key not configured.", "severity": "moderate", "source": "system"}]
    except Exception:
        return [{"name": "Parse Error", "explanation": "Claude API key not configured.", "severity": "moderate", "source": "system"}]
    
    try:
        formatted_chunks = format_chunks_for_prompt(chunks)
        
        prompt = SYSTEM_PROMPT_TEMPLATE.format(
            retrieved_chunks=formatted_chunks,
            user_input=user_input.strip(),
        )
        
        client = Anthropic(api_key=CLAUDE_API_KEY)
        
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1500,
            system=prompt,
            messages=[{"role": "user", "content": "Generate the response."}],
        )
        
        response_text = response.content[0].text.strip()
        
        json_match = response_text.find("{")
        if json_match != -1:
            json_str = response_text[json_match:]
            last_brace = json_str.rfind("}")
            if last_brace != -1:
                json_str = json_str[:last_brace + 1]
            
            parsed = json.loads(json_str)
            conditions = parsed.get("conditions", [])
            if conditions and isinstance(conditions, list):
                return conditions
        
        return [{"name": "Parse Error", "explanation": response_text, "severity": "moderate", "source": "system"}]
    
    except anthropic.APIConnectionError:
        return [{"name": "Parse Error", "explanation": "Failed to connect to Claude API. Please check your internet connection.", "severity": "moderate", "source": "system"}]
    except anthropic.RateLimitError:
        return [{"name": "Parse Error", "explanation": "Rate limit exceeded. Please try again later.", "severity": "moderate", "source": "system"}]
    except json.JSONDecodeError as e:
        return [{"name": "Parse Error", "explanation": f"Failed to parse JSON response: {str(e)}", "severity": "moderate", "source": "system"}]
    except Exception as e:
        return [{"name": "Parse Error", "explanation": f"LLM call failed: {str(e)}", "severity": "moderate", "source": "system"}]