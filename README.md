# 🏥 MedAssist AI — Clinical Symptom Analysis Portal

MedAssist AI is a **state-of-the-art clinical symptom retrieval-augmented generation (RAG) portal**. It provides high-fidelity, evidence-grounded medical symptom evaluations by cross-referencing real-time user symptom inputs with verified healthcare reference guides from institutions like the WHO and NHS.

Featuring a **premium clinical interface** built with Outfit & Inter typography, glowing glassmorphic elements, a simulated live ECG scanner loading wave, soft-triage severity badges, and interactive case dossier slide-overs.

🔗 **Live Production App**: [https://medical-symptom-information-assista.vercel.app](https://medical-symptom-information-assista.vercel.app)

---

## 🎨 Premium Visual & Architectural Features

### 1. Clinical Dashboard Design
*   **Outfit & Inter Typography**: Set up clear, premium, hospital-grade typographic grids.
*   **Heartbeat AI Brandmark**: An active neon-teal pulsating header navigation logo.
*   **ECG Waveform Scanner**: Replaced generic loading spinners with a dark-slate **ECG wave simulation grid** featuring a moving scanning laser dot, active green pulse, and real-time clinical RAG status logs.

### 2. Interactive Clinical Triage
*   **Dynamic Severity Accentuation**: Matched condition cards include left-accented colored sidebar indicators (Crimson for *urgent*, Amber for *moderate*, Emerald for *mild*).
*   **Interactive Triage Badges**: Soft-gradient status pills featuring safety symbols (warning shields or alert pings) indicating emergency statuses.
*   **Verified Medical Citations**: High-trust pills linking and referencing the exact clinical reference guides used (e.g. *WHO Headache Fact Sheet*).

### 3. Patient Case Dossiers
*   Clicking **"View Dossier"** inside the query log slides in a gorgeous medical dossier sheet overlay. This detail panel features evaluation hashes, timestamps, transcripts, full emergency explanation callouts, and structured condition lists.

### 4. Interactive Quick-Start Symptoms
*   Features quick symptom shortcuts (e.g., *Migraine*, *Fever & Dry Cough*, *Itchy Rash*, *Vertigo / Dizziness*) that users can click to pre-fill the symptom description field instantly.

---

## 🛠️ Unified Full-Stack Architecture

```
               ┌────────────────────────────────────────────────────────┐
               │                Vite React SPA Frontend                 │
               └──────────────────────────┬─────────────────────────────┘
                                          │  REST Requests
                                          ▼
               ┌────────────────────────────────────────────────────────┐
               │                FastAPI (Python) Backend                │
               └──────────────────────────┬─────────────────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
┌───────────────────────────────────┐           ┌───────────────────────────────────┐
│       Supabase (PostgreSQL)       │           │        Groq Cloud API             │
│   Evidence Vector Knowledge Base  │           │    Llama-3.3-70B-Versatile LLM    │
└───────────────────────────────────┘           └───────────────────────────────────┘
```

### Modern Cloud Stack
*   **Frontend**: React (Vite) styled with harmonious custom clinical CSS palettes, glowing glassmorphism, and responsive Tailwind UI utilities.
*   **Backend API**: High-performance FastAPI Python app featuring asynchronous query routers and rate limiters.
*   **Database & Search**: Supabase PostgreSQL indexing and querying verified clinical guides.
*   **Large Language Model**: Groq Llama-3.3-70B Cloud API for grounded, evidence-driven symptom assessments.

---

## 🚀 Step-by-Step Vercel Deployment

We bypassed Vercel's strict **50MB size limit** for serverless runtimes by decoupling local offline ML components. In production, MedAssist runs an **extremely fast 15MB cloud pipeline**.

### 1. Unified Routing Configuration (`vercel.json`)
The [vercel.json](vercel.json) at the root level orchestrates both environments:
```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" },
    { "src": "frontend/package.json", "use": "@vercel/static-build", "config": { "distDir": "dist" } }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "api/index.py" },
    { "src": "/assets/(.*)", "dest": "frontend/assets/$1" },
    { "src": "/(.*)", "dest": "frontend/$1", "continue": true }
  ]
}
```

### 2. Live Cloud Environment Variables
In your Vercel Dashboard, go to **Settings ➡️ Environment Variables** and add:
*   `GROQ_API_KEY`: `gsk_VSHea...`
*   `GROQ_MODEL`: `llama-3.3-70b-versatile`
*   `SUPABASE_URL`: `https://dpqyzzx...supabase.co`
*   `SUPABASE_KEY`: `eyJhbGciOi...`

### 3. Deploy
Trigger the deployment directly:
```bash
npx vercel --prod
```

---

## 💻 Local Installation & Setup

### Prerequisites
*   **Node.js** v20+
*   **Python** 3.11+
*   **Git**

### 1. Clone & Configure Environment
```bash
git clone https://github.com/MoeenUddin01/Medical-Symptom-Information-Assistant.git
cd Medical-Symptom-Information-Assistant
```

Create a `.env` file in the root folder:
```env
SUPABASE_URL=https://dpqyzzxjkjhjolpdbdbzbx.supabase.co
SUPABASE_KEY=your_supabase_anon_key
GROQ_API_KEY=gsk_your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

### 2. Start the Backend API
```bash
# Set up a python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Start the uvicorn API server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
The FastAPI backend will spin up at **`http://localhost:8000`**.

### 3. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```
The clinical portal will launch locally at **`http://localhost:5173`**.

---

## 🔒 Security & Medical Advisory

*   **REST API Rate Limiting**: The `/api/symptoms` endpoint is secured with a 20 request/minute IP rate limiter via SlowAPI to prevent scraping and abuse.
*   **Interactive Safeguards**: High-contrast, floating emergency alert notices and sticky disclaimers are placed throughout the UI to ensure responsible product deployment.

> [!IMPORTANT]
> **Medical Disclaimer**: MedAssist AI is designed for informational and educational reference purposes only. It is not a substitute for professional clinical judgment, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns. In an emergency, contact local emergency services immediately.

---

## 📄 License
Licensed under the [MIT License](LICENSE).