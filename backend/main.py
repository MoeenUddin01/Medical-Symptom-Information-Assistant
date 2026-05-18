"""
MedAssist API — FastAPI application entry point.

This module initializes the FastAPI application with CORS, rate limiting,
health check endpoint, and the symptoms analysis router.
"""

import logging
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from backend.config import CHROMA_DB_PATH, CLAUDE_API_KEY, FRONTEND_URL
from backend.routers.symptoms import router as symptoms_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="MedAssist API",
    version="1.0.0",
    description="Medical Symptom Information Assistant API — provides symptom analysis using RAG-based medical knowledge retrieval.",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(symptoms_router)


@app.on_event("startup")
async def startup_event():
    """Log application startup information."""
    api_key_status = "set" if CLAUDE_API_KEY else "not set"
    logger.info("MedAssist API started")
    logger.info("ChromaDB path: %s", CHROMA_DB_PATH)
    logger.info("Anthropic API key: %s", api_key_status)


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Dict with status and version information.
    """
    return {"status": "ok", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
