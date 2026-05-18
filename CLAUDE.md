# CLAUDE.md — Medical Symptom Information Assistant
## Project Orchestration Document (Read before every task)

---

## PROJECT OVERVIEW

You are building a production-grade, deployable Medical Symptom Information Assistant.
This is a RAG-based web application. Users describe symptoms in plain language and receive
structured, sourced, responsible health information. The app must never hallucinate medical
facts — every answer must be grounded in pre-loaded verified medical documents.
This is a real-world deployment project. Every file you write must be production quality.

---

## CORE RULES (never violate these)

1. Emergency keywords (chest pain, difficulty breathing, loss of consciousness, stroke,
   not breathing, unresponsive, severe bleeding, seizure) MUST be detected BEFORE the
   RAG pipeline runs. Emergency UI is shown immediately — do not wait for the LLM.
2. The LLM prompt MUST instruct the model to ONLY use retrieved context chunks.
   Never allow the model to add information not present in the retrieved documents.
3. Every single response shown to the user MUST include a visible disclaimer:
   "This tool is for information only and does not replace a doctor."
4. Every condition card MUST show: condition name, plain-language explanation,
   severity badge (Mild / Moderate / Seek Care Urgently), and source document name.
5. No model training is needed. Use prebuilt models only (scispacy NER, sentence-transformers).
6. All secrets (API keys) go in .env files. Never hardcode them.

---

## TECH STACK

| Layer         | Technology                                      |
|---------------|-------------------------------------------------|
| Frontend      | React + Vite + TailwindCSS                      |
| Backend API   | FastAPI (Python)                                |
| NER           | scispacy (en_core_sci_sm) — prebuilt, no training |
| Embeddings    | sentence-transformers (all-MiniLM-L6-v2)        |
| Vector Store  | ChromaDB (local persistent)                     |
| LLM           | Claude API (claude-sonnet-4-20250514)           |
| Deployment    | Docker + Docker Compose                         |
| Reverse Proxy | Nginx                                           |
| Cloud         | Render.com or Railway (backend) + Vercel (frontend) |

---

## PROJECT STRUCTURE

```
medassist/
├── CLAUDE.md                   ← this file
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 ← FastAPI app entry point
│   ├── config.py               ← env vars, constants
│   ├── routers/
│   │   └── symptoms.py         ← POST /api/symptoms endpoint
│   ├── services/
│   │   ├── emergency.py        ← keyword detection (runs first)
│   │   ├── ner.py              ← scispacy entity extraction
│   │   ├── retrieval.py        ← ChromaDB vector search
│   │   └── llm.py              ← Claude API call + prompt builder
│   ├── ingestion/
│   │   ├── ingest.py           ← load, chunk, embed, store documents
│   │   └── documents/          ← raw medical PDFs/text files go here
│   └── tests/
│       ├── test_emergency.py
│       ├── test_ner.py
│       └── test_retrieval.py
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── api/
│       │   └── symptoms.js     ← fetch wrapper for backend
│       ├── components/
│       │   ├── SymptomInput.jsx
│       │   ├── EmergencyBanner.jsx
│       │   ├── ConditionCard.jsx
│       │   ├── SeverityBadge.jsx
│       │   ├── Disclaimer.jsx
│       │   └── LoadingState.jsx
│       └── pages/
│           └── Home.jsx
│
└── nginx/
    └── nginx.conf
```

---

## PHASES — DO THEM IN ORDER

### PHASE 1 — Project Scaffold & Config
Files: folder structure, .gitignore, .env.example, docker-compose.yml,
backend/config.py, backend/requirements.txt, frontend/package.json

### PHASE 2 — Knowledge Base Ingestion Pipeline
Files: backend/ingestion/ingest.py
Downloads WHO/NHS documents, chunks them (~400 words), embeds with
sentence-transformers, stores in ChromaDB with source metadata.
Run once before the app starts.

### PHASE 3 — Backend Services (core logic)
Files: backend/services/emergency.py, ner.py, retrieval.py, llm.py
Each service is a standalone module. emergency.py runs first always.

### PHASE 4 — FastAPI Router & Main App
Files: backend/main.py, backend/routers/symptoms.py
Single POST /api/symptoms endpoint. Orchestrates the 4-step pipeline.

### PHASE 5 — Frontend Components
Files: all frontend/src/components/*.jsx and frontend/src/pages/Home.jsx
Medical theme: clean, trustworthy, accessible. Cards per condition.
Emergency banner is red and full-width. Disclaimer always visible.

### PHASE 6 — Backend Tests
Files: backend/tests/*.py
Unit tests for emergency detection, NER extraction, retrieval quality.

### PHASE 7 — Docker & Nginx
Files: backend/Dockerfile, frontend/Dockerfile, nginx/nginx.conf,
docker-compose.yml (complete version)

### PHASE 8 — Deployment
Deploy backend to Render.com, frontend to Vercel.
Add environment variable configuration guide.

---

## API CONTRACT

### POST /api/symptoms
Request:
```json
{ "text": "I have chest pain and shortness of breath" }
```

Response (emergency):
```json
{
  "is_emergency": true,
  "emergency_message": "These symptoms may be life-threatening. Call emergency services (115/1122) immediately.",
  "conditions": []
}
```

Response (normal):
```json
{
  "is_emergency": false,
  "emergency_message": null,
  "conditions": [
    {
      "name": "Tension Headache",
      "explanation": "A common headache caused by muscle tension...",
      "severity": "mild",
      "source": "WHO Headache Disorders Fact Sheet"
    }
  ],
  "disclaimer": "This tool is for information only and does not replace a doctor."
}
```

---

## EMERGENCY KEYWORDS LIST

chest pain, difficulty breathing, shortness of breath, loss of consciousness,
unconscious, unresponsive, not breathing, stroke, heart attack, severe bleeding,
coughing blood, seizure, convulsion, anaphylaxis, allergic reaction severe,
cannot breathe, choking, overdose, suicidal, kill myself

---

## SEVERITY RULES FOR LLM PROMPT

- mild: self-care at home, monitor symptoms
- moderate: see a doctor within 24–48 hours
- urgent: seek care today or go to emergency room

---

## LLM SYSTEM PROMPT TEMPLATE (use exactly this structure)

```
You are a medical information assistant. Your only job is to help users understand
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
{"conditions": [{"name": str, "explanation": str, "severity": "mild"|"moderate"|"urgent", "source": str}]}

CONTEXT:
{retrieved_chunks}

USER SYMPTOMS:
{user_input}
```

---

## CODING STANDARDS

- Python: type hints on all functions, docstrings on all classes, black formatting
- React: functional components only, no class components, PropTypes on all components
- All API calls wrapped in try/catch with proper error states in UI
- No TODO comments in final code — finish every function completely
- Environment variables loaded from .env via python-dotenv (backend) and Vite (frontend)
- CORS configured to allow only the frontend origin in production

---

## DOCUMENT SOURCES FOR KNOWLEDGE BASE

These are free, publicly available medical references:
1. WHO Fact Sheets — https://www.who.int/news-room/fact-sheets
2. NHS Health A–Z — https://www.nhs.uk/conditions/
3. MedlinePlus — https://medlineplus.gov/
4. CDC Health Topics — https://www.cdc.gov/az/

Recommended topics to ingest: headache, fever, chest pain, cough, rash, diarrhea,
nausea, dizziness, back pain, sore throat, shortness of breath, fatigue, joint pain,
abdominal pain, eye infection, skin infection, diabetes symptoms, hypertension symptoms.

---

## DEPLOYMENT CHECKLIST

- [ ] .env.example committed, .env in .gitignore
- [ ] CORS restricted to frontend domain
- [ ] Emergency check tested with all keywords
- [ ] Disclaimer visible on every response in UI
- [ ] ChromaDB volume persisted in Docker
- [ ] API rate limiting added (slowapi)
- [ ] Health check endpoint GET /health returns 200
- [ ] Frontend .env.production has correct backend URL
- [ ] Docker images build without errors
- [ ] All tests pass before deploy

---

*Last updated: Phase 0 — Orchestration Setup*
*Agent: Read this file fully before starting any task.*
*Never skip a phase. Complete each phase fully before moving to the next.*