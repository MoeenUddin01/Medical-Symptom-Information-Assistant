# Medical Symptom Information Assistant

A RAG-based web application that helps users understand their symptoms using verified medical reference documents. Users describe symptoms in plain language and receive structured, sourced, responsible health information.

## Project Overview

This application provides medical symptom information by:
1. Detecting emergency keywords before processing
2. Extracting medical entities using scispacy NER
3. Retrieving relevant medical context from a ChromaDB vector store
4. Generating responses using Claude API with grounded medical facts

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Vite + TailwindCSS |
| Backend API | FastAPI (Python) |
| NER | scispacy (en_core_sci_sm) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB |
| LLM | Claude API (claude-sonnet-4-20250514) |

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker (optional, for containerized deployment)

## Installation

### Backend

```bash
pip install -r backend/requirements.txt
python -m spacy download en_core_sci_sm
```

### Frontend

```bash
cd frontend
npm install
```

## Environment Variables

Create a `.env` file in the project root:

```env
# ChromaDB
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=medical_symptoms

# Frontend
FRONTEND_URL=http://localhost:5173

# Embedding Model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Claude API
CLAUDE_API_KEY=your_anthropic_api_key_here
CLAUDE_MODEL=claude-sonnet-4-20250514
```

## Running the Application

### 1. Ingest Medical Knowledge Base

Before running the app, populate the vector store with medical documents:

```bash
python -m backend.ingestion.ingest
```

This builds the knowledge base for 6 topics: headache, fever, cough, rash, nausea, dizziness.

### 2. Start Backend

```bash
python backend/main.py
```

Or with uvicorn directly:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start Frontend

```bash
cd frontend
npm run dev
```

## API Endpoints

### GET /health

Health check endpoint (no rate limit).

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### POST /api/symptoms

Analyze user-reported symptoms (rate limited: 20 requests/minute per IP).

**Request:**
```json
{
  "text": "I have a severe headache and fever"
}
```

**Response (Emergency):**
```json
{
  "is_emergency": true,
  "emergency_message": "These symptoms may indicate a life-threatening emergency. Call emergency services immediately (e.g. 115, 1122, 911). Do not wait.",
  "conditions": [],
  "disclaimer": "This tool is for information only and does not replace a doctor. Always consult a qualified healthcare professional for medical advice."
}
```

**Response (Normal):**
```json
{
  "is_emergency": false,
  "emergency_message": null,
  "conditions": [
    {
      "name": "Tension Headache",
      "explanation": "A common type of headache caused by muscle tension...",
      "severity": "mild",
      "source": "WHO Headache Fact Sheet"
    }
  ],
  "disclaimer": "This tool is for information only and does not replace a doctor. Always consult a qualified healthcare professional for medical advice."
}
```

## Project Structure

```
├── backend/
│   ├── config.py             # Configuration and constants
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── routers/
│   │   └── symptoms.py       # POST /api/symptoms endpoint
│   ├── services/
│   │   ├── emergency.py      # Emergency keyword detection (runs first)
│   │   ├── ner.py            # scispacy entity extraction
│   │   ├── retrieval.py      # ChromaDB vector search
│   │   └── llm.py            # Claude API integration
│   ├── ingestion/
│   │   ├── ingest.py         # Knowledge base build script
│   │   └── documents/        # Raw medical documents
│   └── tests/
│       ├── conftest.py           # Pytest fixtures
│       ├── test_emergency.py     # Emergency detection tests
│       ├── test_ner.py           # NER extraction tests
│       └── test_retrieval.py     # Vector retrieval tests
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Disclaimer.jsx       # Always-visible medical disclaimer banner
│   │   │   ├── EmergencyBanner.jsx   # Red emergency alert with pulsing dot
│   │   │   ├── SymptomInput.jsx      # Symptom input form with validation
│   │   │   ├── ConditionCard.jsx    # Card displaying condition info
│   │   │   ├── SeverityBadge.jsx    # Severity indicator (mild/moderate/urgent)
│   │   │   └── LoadingState.jsx     # Analysis loading animation
│   │   ├── pages/
│   │   │   └── Home.jsx             # Main page orchestrating all components
│   │   ├── api/
│   │   │   └── symptoms.js          # API client for backend
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── ...
├── nginx/
│   └── nginx.conf                   # Reverse proxy config
└── docker-compose.yml               # Container orchestration
```

## Pipeline Order

The symptom analysis pipeline executes in this strict order:
1. **Emergency Detection** — Keyword check (returns immediately if emergency)
2. **NER Extraction** — scispacy extracts symptoms, body parts, conditions
3. **Query Building** — Combines entities with original text
4. **Vector Retrieval** — ChromaDB returns relevant medical chunks
5. **LLM Generation** — Claude generates grounded response

## Emergency Keywords

The system detects these keywords before processing:
- chest pain, difficulty breathing, shortness of breath
- loss of consciousness, unresponsive, not breathing
- stroke, heart attack, severe bleeding
- seizure, convulsion, anaphylaxis
- choking, overdose, suicidal, kill myself

## Security Features

- **CORS** — Restricted to configured frontend origin only
- **Rate Limiting** — 20 requests per minute per IP on `/api/symptoms`
- **API Key Protection** — Never logged or exposed in responses
- **Error Handling** — Internal errors never exposed to clients

## Testing

Run the backend test suite with pytest:

```bash
python3 -m pytest backend/tests/ -v
```

Individual test suites:
```bash
python3 -m pytest backend/tests/test_emergency.py -v
python3 -m pytest backend/tests/test_ner.py -v
python3 -m pytest backend/tests/test_retrieval.py -v
```

Tests are fully mocked and do not require a running database or external services.

## Disclaimer

This tool is for information only and does not replace a doctor. Always consult a qualified healthcare professional for medical advice.

## License

MIT