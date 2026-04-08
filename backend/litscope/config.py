"""
config.py — Global configuration, the single source of truth for all constants
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ──────────────────────────────────────────────────────────────────
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# ── Journal configuration ─────────────────────────────────────────────────────
JOURNALS = [
    {
        "name":        "Information Systems Research",
        "short":       "ISR",
        "openalex_id": "S202812398",
        "issn":        "1047-7047",
        "platform":    "INFORMS / ISR",
        "max":         3000,
    },
    {
        "name":        "MIS Quarterly",
        "short":       "MISQ",
        "openalex_id": "S57293258",
        "issn":        "0276-7783",
        "platform":    "AIS / MISQ",
        "max":         2000,
    },
    {
        "name":        "Journal of Management Information Systems",
        "short":       "JMIS",
        "openalex_id": "S9954729",
        "issn":        "0742-1222",
        "platform":    "Taylor & Francis / JMIS",
        "max":         2000,
    },
]

# ── Platform mapping ─────────────────────────────────────────────────────────
VENUE_PLATFORM_MAP = {j["name"]: j["platform"] for j in JOURNALS}

PLATFORM_ORDER = [j["platform"] for j in JOURNALS]

# ── OpenAlex fetch parameters ─────────────────────────────────────────────────
OPENALEX_USER_AGENT = "LitScope/1.0 (Academic Research; mailto:researcher@email.com)"
FETCH_BATCH         = 200

# ── Data paths ────────────────────────────────────────────────────────────────
DATA_DIR        = "data"
RAW_CSV         = f"{DATA_DIR}/papers_raw.csv"
CLASSIFIED_CSV  = f"{DATA_DIR}/papers_classified.csv"
BY_PLATFORM_CSV = f"{DATA_DIR}/papers_by_platform.csv"
BY_PLATFORM_DIR = f"{DATA_DIR}/by_platform"
EMBEDDINGS_FILE  = f"{DATA_DIR}/papers_embeddings.npy"
FINETUNED_MODEL  = f"{DATA_DIR}/models/specter-is-finetuned"

# ── CSV column order ──────────────────────────────────────────────────────────
CSV_COLUMNS = [
    "title", "abstract", "year", "venue", "authors",
    "doi", "url", "source", "platform",
    "is_behavioral", "theories_used", "confidence", "reason",
]
