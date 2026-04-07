# LitScope — IS Literature Explorer

A semantic search and classification tool for Information Systems academic literature.
Users describe what they're looking for in natural language, and LitScope finds relevant papers by meaning — not just keywords.

---

## What It Does

- **Classifies** 5,451 papers from ISR, MISQ, and JMIS — 1,510 identified as behavioral IS research (27.7%)
- **Semantic search** powered by SPECTER embeddings — finds papers by concept, not exact wording
- **Theory-aware ranking** — boosts papers that match the theoretical framework mentioned in the query
- **Dashboard** with publication trends, platform distribution, and top theories

---

## Architecture

```
OpenAlex API
    ↓
papers_raw.csv  (title, abstract, year, DOI, venue)
    ↓
SPECTER Embeddings  (768-dim semantic vectors, allenai-specter)
    ↓
LLM Classification  (DeepSeek + GPT-OSS-120B + Llama-3.3-70B, majority vote)
    ↓
papers_classified.csv  (is_behavioral, theories_used, confidence, reason)
    ↓
FastAPI backend  +  React frontend
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Data source | OpenAlex API (free, no key required) |
| Embeddings | SPECTER (`allenai-specter`) via sentence-transformers |
| Classification | DeepSeek API (primary), OpenRouter, Groq |
| Backend | FastAPI + Python |
| Frontend | React 18 + Vite + Recharts |
| Journals covered | ISR (INFORMS), MISQ (AIS), JMIS (Taylor & Francis) |

---

## Project Structure

```
LitScope/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── requirements.txt
│   ├── data/                    # CSV data files (git-ignored)
│   │   ├── papers_classified.csv
│   │   ├── papers_embeddings.npy
│   │   └── by_platform/
│   ├── litscope/
│   │   ├── config.py            # Paths, API keys, journal definitions
│   │   ├── fetcher.py           # OpenAlex API client
│   │   ├── classifier.py        # LLM classification logic
│   │   ├── searcher.py          # SPECTER semantic search
│   │   ├── organizer.py         # Data merging and sorting
│   │   └── storage.py           # CSV read/write
│   ├── routers/
│   │   ├── papers.py            # GET /api/papers
│   │   ├── search.py            # GET/POST /api/search
│   │   ├── stats.py             # GET /api/stats
│   │   └── jobs.py              # POST /api/jobs/*
│   └── services/
│       └── job_runner.py        # Background job execution
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── api.js               # All API calls
│       ├── components/          # FilterBar, PaperTable, PaperDetail, charts
│       └── pages/               # Dashboard, Search, Browse, Jobs
└── colab/
    ├── 01_fetch_papers.ipynb    # Fetch from OpenAlex
    └── 02_classify_papers.ipynb # SPECTER + LLM classification pipeline
```

---

## Getting Started

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:
```
DEEPSEEK_API_KEY=your_key_here
```

Place your data files in `backend/data/`:
- `papers_classified.csv`
- `papers_embeddings.npy`

Start the server:
```bash
PYTHONPATH=. uvicorn main:app --reload
```

API available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search?q=...&top_k=10&only_behavioral=false` | Semantic search |
| GET | `/api/papers` | List papers with filters |
| GET | `/api/papers/{doi}` | Get paper by DOI |
| GET | `/api/stats` | Aggregate statistics |
| POST | `/api/jobs/fetch` | Fetch new papers from OpenAlex |
| POST | `/api/jobs/classify` | Run LLM classification |
| POST | `/api/jobs/sort` | Sort and split by platform |

---

## Classification Pipeline (Colab)

The classification pipeline runs in Google Colab. SPECTER encoding benefits from a GPU but also runs on CPU (slower):

1. **`01_fetch_papers.ipynb`** — Pulls papers from OpenAlex, saves to `papers_raw.csv`
2. **`02_classify_papers.ipynb`** — Encodes with SPECTER, classifies with LLMs, validates results

Required Colab secrets:
- `DEEPSEEK_API_KEY`
- `OPENROUTER_API_KEY` (for validation with GPT-OSS-120B)
- `GROQ_API_KEY` (for validation with Llama-3.3-70B)

---

## Search Scoring

Semantic search uses a hybrid scoring formula:

```
final_score = cosine_similarity + behavioral_boost + theory_match_bonus
```

- **`behavioral_boost`**: +0.12 for high-confidence behavioral papers, +0.06 for medium
- **`theory_match_bonus`**: +0.08 per theory name found in both query and paper (capped at 2)

This ensures behavioral papers and theory-specific papers rank above equally similar non-behavioral papers.

---

## Data

All data is sourced from [OpenAlex](https://openalex.org) (open access, no registration required).

| Journal | Papers | Behavioral |
|---------|--------|-----------|
| Information Systems Research (ISR) | 1,672 | 424 (25.4%) |
| MIS Quarterly (MISQ) | 2,195 | 645 (29.4%) |
| Journal of MIS (JMIS) | 1,584 | 441 (27.8%) |
| **Total** | **5,451** | **1,510 (27.7%)** |

---

## License

MIT
