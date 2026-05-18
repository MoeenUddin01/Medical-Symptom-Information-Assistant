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

from backend.config import FRONTEND_URL, SUPABASE_KEY, SUPABASE_URL
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(symptoms_router)


@app.on_event("startup")
async def startup_event():
    """Log application startup information."""
    logger.info("MedAssist API started")

    if SUPABASE_URL and SUPABASE_KEY:
        logger.info("Supabase connected: %s", SUPABASE_URL)

        from backend.services.knowledge import get_knowledge_count, seed_knowledge_base, MEDICAL_DOCUMENTS

        count = get_knowledge_count()
        logger.info("Knowledge base count: %d", count)

        if count == 0:
            logger.info("Seeding knowledge base...")
            seeded = seed_knowledge_base(MEDICAL_DOCUMENTS)
            logger.info("Seeded %d knowledge chunks", seeded)
    else:
        logger.warning("Supabase not configured - query logging disabled")


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