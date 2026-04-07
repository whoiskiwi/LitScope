# LitScope — System Design

## Project Goal

Users describe what type of papers they are looking for, and the system precisely retrieves matching papers from multiple academic journals.
The system goes beyond keyword matching — it genuinely understands a paper's theoretical foundation and research methodology.
The design is domain-agnostic: IS, NeurIPS, medical research, or any other field can be plugged in, with user-defined query dimensions.

---

## Architecture Overview

```
[Phase 1: Data Pipeline]  ← current phase
──────────────────────────────────────────────────
OpenAlex API
    ↓ fetch full paper metadata
papers_raw.csv  (title + abstract + year + DOI)
    ↓
SPECTER Embedding  (SciBERT variant, pre-trained on academic corpora)
    ↓ each paper → semantic vector
papers_embeddings.npy  (reserved for downstream use)
    ↓
3-model voting classification  (DeepSeek × GPT-OSS-120B × Llama-3.3-70B)
    ↓ majority vote + confidence level
papers_classified.csv  (labelled structured dataset)

[Phase 2: ML Classifier Training]  ← next phase
──────────────────────────────────────────────────
papers_classified.csv  (LLM labels as training data)
    ↓ 80/20 train/test split
SPECTER vectors (features) + is_behavioral label (target)
    ↓ train lightweight classifier  (Logistic Regression / SVM / MLP)
Evaluation: accuracy / recall / precision / loss curve
    ↓
Lightweight classifier model  (runs locally, no API required)

[Phase 3: User Query Interface]  ← future extension
──────────────────────────────────────────────────
User natural language input
    ↓ convert to SPECTER vector
Vector database semantic retrieval  (ChromaDB / FAISS)  top-N candidates
    ↓
LLM re-ranking → display results
```

---

## Layer Details

### Layer 1: Data Ingestion

**Tool: OpenAlex API**

- **What it is**: Free academic paper database covering metadata for virtually all major journals
- **Fields fetched**: title, abstract, year, authors, DOI, journal name
- **Why**: Completely free, no registration, simple API, full coverage of ISR / MISQ / JMIS

Journals currently integrated:

| Journal | OpenAlex ID | max |
|---------|-------------|-----|
| Information Systems Research (ISR) | S202812398 | 3000 |
| MIS Quarterly (MISQ) | S57293258 | 2000 |
| Journal of Management Information Systems (JMIS) | S9954729 | 2000 |

---

### Layer 2: Semantic Understanding (Embedding)

**Tool: SPECTER (`allenai-specter`)**

- **What it is**: A SciBERT-based model fine-tuned on academic paper citation pairs
- **Role**: Converts paper title + abstract into high-dimensional semantic vectors, stored in `papers_embeddings.npy`
- **Current status**: Vectors generated and saved
- **Runtime**: Runs locally in Colab, free, no API calls

**Three planned uses of the vectors (by phase):**

| Phase | Use |
|-------|-----|
| Phase 2 | Input features for ML classifier |
| Phase 3 | Semantic search: user query → find similar papers |
| Phase 3 | UMAP / t-SNE dimensionality reduction for paper map visualisation |

---

### Layer 3: 3-Model Voting Classification (current core)

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

**Value of Prompt B**: Even when a paper does not explicitly name a theory, GPT-OSS and Llama can infer a behavioral foundation from the research methods (survey, SEM, human-subjects study), compensating for the limitations of pure keyword matching.

**API Key setup (Colab Secrets):**

| Secret | Source |
|--------|--------|
| `DEEPSEEK_API_KEY` | platform.deepseek.com |
| `OPENROUTER_API_KEY` | openrouter.ai (free) |
| `GROQ_API_KEY` | console.groq.com (free) |

---

### Layer 4: Full Validation (post-classification)

**Method: keyword cross-validation** (theory keyword list kept in sync with prompts)

- **Recall**: Among papers whose abstracts contain explicit theory keywords, the % correctly predicted True
- **Precision**: Among papers predicted True, the % with keyword evidence
- **Limitation**: Only validates papers that explicitly name a theory; papers applying behavioral theory without naming it require manual spot-checking

---

### Layer 5: ML Classifier Training (next phase)

**Goal**: Use LLM labels to train a lightweight classifier — enabling local inference without API calls

**Pipeline:**

```
papers_classified.csv  (LLM-labelled, 5000+ papers)
    ↓
80% train / 20% test  (random split, stratified by is_behavioral)
    ↓
Features: SPECTER vectors  (papers_embeddings.npy)
Labels:   is_behavioral  (True / False)
    ↓
Train classifiers:  Logistic Regression / SVM / MLP
    ↓
Evaluation: Accuracy / Recall / Precision / F1 / Loss curve
```

**Why LLM → ML?**
LLM labels serve as weak supervision training data. Their quality is sufficient to train a lightweight classifier. Once trained, new papers can be classified locally — fast and zero-cost.

---

### Layer 6: User Query Interface (future extension)

**Design principle**: Not bound to fixed classification fields — users define their own query dimensions

**Example queries:**
- "Papers using behavioral theory to predict user decision-making"
- "Papers applying transformers to recommendation systems"
- "IS papers using randomised controlled experiments"

**System flow:**
1. Convert user input to a SPECTER vector
2. Retrieve top-N candidate papers from vector database (semantic coarse filter)
3. LLM re-ranks candidates and filters non-matching results
4. Return results with reasoning

---

## Tool Summary

| Tool | Type | Role | Cost | Runtime |
|------|------|------|------|---------|
| OpenAlex | Data API | Bulk fetch paper metadata | Free | HTTP requests |
| SPECTER | Pre-trained LM | Abstract → semantic vector | Free | Colab local |
| DeepSeek | LLM API | Prompt A classification | ~$1 / full dataset | API call |
| GPT-OSS-120B | LLM API (OpenRouter) | Prompt B classification | Free | API call |
| Llama-3.3-70B | LLM API (Groq) | Prompt B classification | Free | API call |
| Logistic Reg / SVM | ML classifier | Lightweight local classification | Free | Local training |
| ChromaDB / FAISS | Vector database | Store vectors, semantic retrieval | Free | Local |

---

## Roadmap

### Phase 1: Data Pipeline ← current

- [x] OpenAlex journal IDs verified and corrected
- [x] Data fetch script (`01_fetch_papers.ipynb`)
- [x] SPECTER vector generation and save
- [x] 3-model voting classification framework
- [x] Full dataset classified (5,451 papers)
- [x] Full validation (Cell 8 keyword cross-validation)
- [x] Multi-model precision validation (Cell 9, 50-sample spot-check)

### Phase 2: ML Classifier Training

- [ ] 80/20 train/test split (stratified by `is_behavioral`)
- [ ] Train classifier on SPECTER vectors
- [ ] Evaluate: accuracy / recall / F1 / loss curve
- [ ] Compare classifiers (LR vs SVM vs MLP)
- [ ] Save best model

### Phase 3: User Query Interface

- [x] Semantic search API (`/api/search`)
- [x] Theory-aware hybrid scoring (behavioral boost + theory match bonus)
- [x] Search page with natural language chatbox
- [ ] Expand classification to all IS research categories (behavioral, technical, economic, organizational, design science, qualitative, econometric)
- [ ] Vector database integration (ChromaDB or FAISS)
- [ ] Support new domains (NeurIPS, medical, etc.)

### Phase 4: Visualisation

- [ ] UMAP / t-SNE dimensionality reduction — 2D paper map
- [ ] Interactive scatter plot on frontend (click to view paper detail)
- [ ] Colour-coded by platform / year / research type
