"""
LLM integration module for the Medical Symptom Information Assistant.

This module handles calling the Google Gemini API with the retrieved medical context
to generate symptom information responses.

Usage:
    from backend.services.llm import call_llm, build_disclaimer

    conditions = call_llm("I have a severe headache", chunks)
    disclaimer = build_disclaimer()
"""

import json
import re
from typing import Dict, List
import requests

import google.generativeai as genai

from backend.config import GOOGLE_API_KEY, GEMINI_MODEL, GROQ_API_KEY, GROQ_MODEL
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
{retrieved_chunks}

USER SYMPTOMS:
{user_input}"""

_generative_model = None


def _get_model():
    """
    Load and return the Gemini model, configuring the API once at module level.

    Returns:
        The configured GenerativeModel instance.

    Raises:
        RuntimeError: If the API key is not configured or model initialization fails.
    """
    global _generative_model
    if _generative_model is not None:
        return _generative_model

    try:
        if not GOOGLE_API_KEY:
            raise RuntimeError("Google API key not configured. Set GOOGLE_API_KEY in .env")
        genai.configure(api_key=GOOGLE_API_KEY)
        _generative_model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 1500,
            },
        )
        return _generative_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Gemini model: {str(e)}") from e


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
    Call the Google Gemini API with the user's symptoms and retrieved context.

    This function builds a prompt using the exact template from CLAUDE.md,
    sends it to Gemini, and parses the JSON response into condition dictionaries.

    Args:
        user_input: The original user symptom description.
        chunks: List of retrieved document chunks from the retrieval service.

    Returns:
        List of condition dicts with keys: name, explanation, severity, source.
        On any error, returns a single condition dict with name "Parse Error"
        containing the raw model output or error message.
    """
    try:
        if not user_input or not user_input.strip():
            return [
                {
                    "name": "Parse Error",
                    "explanation": "No user input provided.",
                    "severity": "moderate",
                    "source": "system",
                }
            ]
    except Exception as e:
        return [
            {
                "name": "Parse Error",
                "explanation": f"Input validation failed: {str(e)}",
                "severity": "moderate",
                "source": "system",
            }
        ]

    try:
        if not chunks:
            return [
                {
                    "name": "Parse Error",
                    "explanation": "No relevant medical information found.",
                    "severity": "moderate",
                    "source": "system",
                }
            ]
    except Exception as e:
        return [
            {
                "name": "Parse Error",
                "explanation": f"Chunk validation failed: {str(e)}",
                "severity": "moderate",
                "source": "system",
            }
        ]

    try:
        formatted_chunks = format_chunks_for_prompt(chunks)
    except Exception as e:
        return [
            {
                "name": "Parse Error",
                "explanation": f"Failed to format chunks: {str(e)}",
                "severity": "moderate",
                "source": "system",
            }
        ]

    try:
        prompt = SYSTEM_PROMPT_TEMPLATE.format(
            retrieved_chunks=formatted_chunks,
            user_input=user_input.strip(),
        )
    except Exception as e:
        return [
            {
                "name": "Parse Error",
                "explanation": f"Failed to build prompt: {str(e)}",
                "severity": "moderate",
                "source": "system",
            }
        ]

    if GROQ_API_KEY:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 1500,
                "response_format": {"type": "json_object"}
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            raw_text = result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return [
                {
                    "name": "Parse Error",
                    "explanation": f"Groq API call failed: {str(e)}",
                    "severity": "moderate",
                    "source": "system",
                }
            ]
    else:
        try:
            model = _get_model()
        except Exception as e:
            return [
                {
                    "name": "Parse Error",
                    "explanation": f"Model initialization failed: {str(e)}",
                    "severity": "moderate",
                    "source": "system",
                }
            ]

        try:
            response = model.generate_content(prompt)
            raw_text = response.text.strip()
        except Exception as e:
            return [
                {
                    "name": "Parse Error",
                    "explanation": f"Gemini API call failed: {str(e)}",
                    "severity": "moderate",
                    "source": "system",
                }
            ]

    try:
        cleaned_text = _strip_markdown_fences(raw_text)
        parsed = json.loads(cleaned_text)
        conditions = parsed.get("conditions", [])
        if isinstance(conditions, list):
            if len(conditions) == 0:
                return [
                    {
                        "name": "No matching conditions",
                        "explanation": "I could not find specific information about these symptoms in my reference documents. Please consult a healthcare professional for guidance.",
                        "severity": "mild",
                        "source": "System"
                    }
                ]
            
            validated_conditions = []
            for cond in conditions:
                if isinstance(cond, dict) and "name" in cond:
                    validated_conditions.append(
                        {
                            "name": str(cond.get("name", "")),
                            "explanation": str(cond.get("explanation", "")),
                            "severity": str(cond.get("severity", "moderate")),
                            "source": str(cond.get("source", "unknown")),
                        }
                    )
            if validated_conditions:
                return validated_conditions
        return [
            {
                "name": "Parse Error",
                "explanation": raw_text[:500] if raw_text else "Empty response from model",
                "severity": "moderate",
                "source": "system",
            }
        ]
    except json.JSONDecodeError as e:
        return [
            {
                "name": "Parse Error",
                "explanation": f"Failed to parse JSON response: {str(e)}. Raw: {raw_text[:500]}",
                "severity": "moderate",
                "source": "system",
            }
        ]
    except Exception as e:
        return [
            {
                "name": "Parse Error",
                "explanation": f"Unexpected error parsing response: {str(e)}",
                "severity": "moderate",
                "source": "system",
            }
        ]


def _strip_markdown_fences(text: str) -> str:
    """
    Strip markdown code fences from text.

    Removes ```json, ``` and similar fences from the beginning and end of text.

    Args:
        text: The raw text that may contain markdown fences.

    Returns:
        The text with markdown fences removed.
    """
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()