import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "medical_symptoms")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

CHUNK_MIN_WORDS = 350
CHUNK_MAX_WORDS = 450
CHUNK_OVERLAP_WORDS = 50

EMERGENCY_KEYWORDS = [
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "loss of consciousness",
    "unconscious",
    "unresponsive",
    "not breathing",
    "stroke",
    "heart attack",
    "severe bleeding",
    "coughing blood",
    "seizure",
    "convulsion",
    "anaphylaxis",
    "allergic reaction severe",
    "cannot breathe",
    "choking",
    "overdose",
    "suicidal",
    "kill myself",
]
