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
cd backend
pip install -r requirements.txt
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

This downloads medical text for 6 topics: headache, fever, cough, rash, nausea, dizziness.

### 2. Start Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 3. Start Frontend

```bash
cd frontend
npm run dev
```

## API Endpoint

### POST /api/symptoms

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
  "conditions": []
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
      "explanation": "A common type of headache...",
      "severity": "mild",
      "source": "WHO Headache Fact Sheet"
    }
  ],
  "disclaimer": "This tool is for information only and does not replace a doctor."
}
```

## Project Structure

```
├── backend/
│   ├── config.py           # Configuration and constants
│   ├── main.py             # FastAPI application
│   ├── routers/
│   │   └── symptoms.py     # API endpoint handlers
│   ├── services/
│   │   ├── emergency.py    # Emergency keyword detection
│   │   ├── ner.py          # Named entity recognition
│   │   ├── retrieval.py    # Vector store queries
│   │   └── llm.py          # Claude API integration
│   ├── ingestion/
│   │   ├── ingest.py       # Knowledge base build script
│   │   └── documents/      # Raw medical documents
│   └── tests/              # Unit tests
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── api/            # API client
│   └── ...
├── nginx/
│   └── nginx.conf          # Reverse proxy config
└── docker-compose.yml     # Container orchestration
```

## Emergency Keywords

The system detects these keywords before processing:
- chest pain, difficulty breathing, shortness of breath
- loss of consciousness, unresponsive, not breathing
- stroke, heart attack, severe bleeding
- seizure, convulsion, anaphylaxis
- choking, overdose, suicidal

## Disclaimer

This tool is for information only and does not replace a doctor. Always consult a qualified healthcare professional for medical advice.

## License

MIT