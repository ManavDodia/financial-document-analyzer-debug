# Financial Document Analyzer — Fixed Edition

A FastAPI + CrewAI system that analyzes financial PDF documents using LLM-based agents.

---

## 🔧 Bugs Found & How You Fixed Them

- General fixes applied across the codebase to ensure the service runs end-to-end.


---

## 🚀 Setup & Usage

### 1) Environment

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Configure Environment
Create a `.env` in project root:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
SERPER_API_KEY=your-serper-key  # optional
```

### 3) Run the API

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to test.


---

## 📑 API Documentation

### GET /
Health check.

**Response**
```json
{ "message": "Financial Document Analyzer API is running" }
```

### POST /analyze
Analyze a financial document.

**Request**: `multipart/form-data`
- `file` (PDF, required)
- `query` (string, optional)

**Response**: `application/json`
```json
{
  "query": "Summarize risks from this report",
  "analysis": "<structured analysis text>",
  "file_processed": "Tesla-Q2-2025.pdf"
}
