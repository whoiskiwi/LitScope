# LitScope — System Design

## Project Goal

Users describe what type of papers they are looking for, and the system precisely retrieves matching papers from multiple academic journals.
The system goes beyond keyword matching — it genuinely understands a paper's theoretical foundation and research methodology.
The design is domain-agnostic: IS, NeurIPS, medical research, or any other field can be plugged in, with user-defined query dimensions.

---

## Architecture Overview

```
[Phase 1: Data Pipeline]  ✅ complete
──────────────────────────────────────────────────
OpenAlex API
    ↓ fetch full paper metadata
papers_raw.csv  (title + abstract + year + DOI + venue + authors)
    ↓
3-model voting classification  (DeepSeek × GPT-OSS-120B × Llama-3.3-70B)
    ↓ majority vote + confidence level
papers_classified.csv  (5,451 papers labelled with is_behavioral + theories_used)

[Phase 2: SPECTER Fine-Tuning + ML Classifier]  ✅ complete
──────────────────────────────────────────────────
papers_classified.csv  (LLM labels as weak supervision)
    ↓ generate synthetic query pairs  (03_generate_queries.ipynb)
synthetic_queries.csv
    ↓ fine-tune SPECTER on IS-domain pairs  (04_finetune_specter.ipynb)
specter-is-finetuned/  (domain-adapted sentence transformer)
    ↓ encode all papers → vectors
papers_embeddings.npy
    ↓ 80/20 stratified split, train classifiers  (05_train_classifier.ipynb)
behavioral_classifier.pkl  (best model saved, used by backend)

[Phase 3: User Query Interface]  🚧 in progress
──────────────────────────────────────────────────
User natural language input
    ↓ encode with specter-is-finetuned
cosine similarity over papers_embeddings.npy
    ↓ hybrid scoring: similarity + behavioral_boost + theory_match_bonus
top-N results  →  FastAPI /api/search  →  React frontend

[Phase 4: Visualisation]  ⬜ planned
──────────────────────────────────────────────────
papers_embeddings.npy
    ↓ UMAP / t-SNE dimensionality reduction
2D coordinates  →  interactive scatter plot  →  click to view paper detail
```

---

## Layer Details

### Layer 1: Data Ingestion

**Tool: OpenAlex API**

- **What it is**: Free academic paper database covering metadata for virtually all major journals
- **Fields fetched**: title, abstract, year, authors, DOI, journal name, URL
- **Why**: Completely free, no registration, simple API, full coverage of ISR / MISQ / JMIS

Journals currently integrated:

| Journal | OpenAlex ID | Max |
|---------|-------------|-----|
| Information Systems Research (ISR) | S202812398 | 3,000 |
| MIS Quarterly (MISQ) | S57293258 | 2,000 |
| Journal of Management Information Systems (JMIS) | S9954729 | 2,000 |

---

### Layer 2: 3-Model Voting Classification

**Tools: DeepSeek × GPT-OSS-120B × Llama-3.3-70B**

| Model | API | Prompt | Angle |
|-------|-----|--------|-------|
| DeepSeek | api.deepseek.com | Prompt A (theory-first) | Looks for theory names + hypothesis language |
| GPT-OSS-120B | OpenRouter (free) | Prompt B (method-first) | Infers behavioral theory from research methods |
| Llama-3.3-70B | Groq (free) | Prompt B (method-first) | Independent second opinion |

**Voting rules:**

| Outcome | Confidence |
|---------|-----------|
| All 3 agree True | high |
| 2/3 agree True | medium |
| All 3 agree False | high |
| 2/3 agree False | medium |
| Tie / all errors | uncertain |

**Result**: 5,451 papers classified, stored in `papers_classified.csv` with fields:
`is_behavioral`, `theories_used`, `confidence`, `reason`

---

### Layer 3: Keyword Cross-Validation

**Method**: Theory keyword list kept in sync with prompts

- **Recall**: Among papers whose abstracts contain explicit theory keywords, the % correctly predicted True
- **Precision**: Among papers predicted True, the % with keyword evidence
- **50-sample manual spot-check** (Cell 9) for papers applying theory without naming it

---

### Layer 4: SPECTER Fine-Tuning (beyond original design)

**Goal**: Adapt SPECTER's generic academic embeddings to IS-domain semantics

**Pipeline** (`colab/fine-tuning/`):

```
papers_classified.csv
    ↓ 03_generate_queries.ipynb
    Sample behavioral papers → generate synthetic natural language queries via LLM
    Output: synthetic_queries.csv  (query ↔ paper pairs)
    ↓ 04_finetune_specter.ipynb
    Fine-tune allenai-specter on (query, positive_paper, negative_paper) triplets
    Output: specter-is-finetuned/  (saved as SentenceTransformer)
```

**Why fine-tune?**
Pre-trained SPECTER was trained on citation pairs — it understands "similar papers". Fine-tuning on IS query/paper pairs teaches it to bridge the gap between a user's natural language question and IS academic writing style.

---

### Layer 5: ML Classifier Training

**Goal**: Use LLM labels + fine-tuned embeddings to train a lightweight local classifier

**Pipeline** (`colab/fine-tuning/05_train_classifier.ipynb`):

```
papers_classified.csv  +  specter-is-finetuned embeddings
    ↓ 80% train / 20% test  (stratified by is_behavioral)
    ↓ train classifiers: Logistic Regression / SVM / MLP
    ↓ Evaluate: Accuracy / Recall / Precision / F1 / Loss curve
behavioral_classifier.pkl  (best model saved)
```

**Status**: Complete. Model saved to `backend/data/models/behavioral_classifier.pkl`.

---

### Layer 6: Semantic Search API

**Scoring formula** (`litscope/searcher.py`):

```
final_score = cosine_similarity(query_vec, paper_vec)
            + behavioral_boost      # +0.12 (high conf) / +0.06 (medium conf)
            + theory_match_bonus    # +0.08 per matched theory (capped at 2)
```

**Theory detection**: 22 canonical IS theories mapped to query-side aliases (TAM, UTAUT, TPB, Privacy Calculus, etc.)

**Endpoints** (`/api/search`):
- `POST /api/search` — main search, accepts `query`, `top_k`, `only_behavioral`
- `GET /api/search` — same via query params
- `GET /api/search/examples` — returns dynamic example queries from high-confidence behavioral papers

**Stats endpoint** (`/api/stats`):
- Total papers, behavioral %, breakdown by platform and year
- Top 10 theories with name canonicalization

---

### Layer 7: Frontend

**Pages** (`frontend/src/pages/`):

| Page | Description |
|------|-------------|
| DashboardPage | Hero intro + stats overview + video demo |
| SearchPage | Natural language chatbox + result cards |
| BrowsePage | Full paper table with filtering |
| JobsPage | Background job monitoring |

**Components**: `PaperDetail`, `PaperTable`, `FilterBar`, `PlatformChart`, `YearChart`, `StatCard`, `JobStatusBadge`

---

## Tool Summary

| Tool | Type | Role | Cost | Runtime |
|------|------|------|------|---------|
| OpenAlex | Data API | Bulk fetch paper metadata | Free | HTTP requests |
| DeepSeek | LLM API | Prompt A classification | ~$1 / full dataset | API call |
| GPT-OSS-120B | LLM API (OpenRouter) | Prompt B classification | Free | API call |
| Llama-3.3-70B | LLM API (Groq) | Prompt B classification | Free | API call |
| allenai-specter | Pre-trained LM | Base model for fine-tuning | Free | Colab local |
| specter-is-finetuned | Fine-tuned LM | Query/paper encoding for search | Free | Local inference |
| Logistic Reg / SVM / MLP | ML classifier | Lightweight local classification | Free | Local training |
| behavioral_classifier.pkl | Trained model | Classify new papers without API | Free | Local inference |

---

## Roadmap

### Phase 1: Data Pipeline ✅ Complete

- [x] OpenAlex journal IDs verified and corrected
- [x] Data fetch script (`01_fetch_papers.ipynb`)
- [x] 3-model voting classification framework
- [x] Full dataset classified (5,451 papers)
- [x] Full validation (keyword cross-validation)
- [x] Multi-model precision validation (50-sample spot-check)

### Phase 2: SPECTER Fine-Tuning + ML Classifier ✅ Complete

- [x] Synthetic query generation (`03_generate_queries.ipynb`)
- [x] SPECTER fine-tuned on IS domain (`04_finetune_specter.ipynb`)
- [x] 80/20 stratified train/test split (`05_train_classifier.ipynb`)
- [x] Train classifiers (LR / SVM / MLP), evaluate accuracy / recall / F1
- [x] Best model saved (`behavioral_classifier.pkl`)
- [x] Fine-tuned embeddings saved (`papers_embeddings.npy`)

### Phase 3: User Query Interface 🚧 In Progress

- [x] Semantic search API (`/api/search`) with GET + POST
- [x] Theory-aware hybrid scoring (behavioral boost + theory match bonus)
- [x] Search page with natural language chatbox
- [x] Dashboard with stats (total, behavioral %, by platform, by year, top theories)
- [x] Browse page (full paper table + filtering)
- [x] Paper detail view
- [x] Example queries endpoint (dynamic, similarity-ranked)
- [x] Video demo on dashboard
- [ ] Expand classification to more IS dimensions (methodology, technology type, industry, theoretical lens)
- [ ] Vector database integration (ChromaDB or FAISS) to replace brute-force cosine search
- [ ] Support new domains (NeurIPS, medical, etc.) with domain-specific models

### Phase 4: Visualisation ⬜ Planned

- [ ] UMAP / t-SNE dimensionality reduction — 2D paper map
- [ ] Interactive scatter plot on frontend (click to view paper detail)
- [ ] Colour-coded by platform / year / research type / theory
