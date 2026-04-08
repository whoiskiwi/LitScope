"""
searcher.py — Semantic search using SPECTER embeddings.

Scoring formula:
    final = semantic_similarity + behavioral_boost + theory_match_bonus

    behavioral_boost:
        behavioral + high confidence   → BEHAVIORAL_BOOST
        behavioral + medium confidence → BEHAVIORAL_BOOST * 0.5
        non-behavioral                 → 0

    theory_match_bonus:
        query contains a theory name that appears in paper's theories_used
        → THEORY_MATCH_BONUS per matched theory (capped at 2 theories)
"""

import os
import re
import numpy as np
import pandas as pd
from litscope.config import CLASSIFIED_CSV, EMBEDDINGS_FILE, FINETUNED_MODEL

# ── Tunable weights ────────────────────────────────────────────────────────────
BEHAVIORAL_BOOST  = 0.12   # added to score for behavioral papers (high conf)
THEORY_MATCH_BONUS = 0.08  # added when query explicitly names a theory in the paper

# Theory aliases for query-side detection
# key = canonical name (must appear as substring in theories_used column)
# values = terms to look for in the user query
_THEORY_ALIASES: dict[str, list[str]] = {
    "TAM":                         ["tam", "technology acceptance", "perceived usefulness", "perceived ease"],
    "TPB":                         ["tpb", "theory of planned behavior", "planned behaviour"],
    "TRA":                         ["tra", "theory of reasoned action", "reasoned action"],
    "UTAUT":                       ["utaut", "unified theory of acceptance"],
    "Prospect Theory":             ["prospect theory", "loss aversion"],
    "Bounded Rationality":         ["bounded rationality", "satisficing"],
    "Mental Accounting":           ["mental accounting"],
    "Framing Effects":             ["framing effect", "framing"],
    "Anchoring":                   ["anchoring"],
    "Self-Determination Theory":   ["sdt", "self-determination", "intrinsic motivation", "extrinsic motivation"],
    "Regulatory Focus Theory":     ["regulatory focus", "promotion focus", "prevention focus"],
    "Goal-Setting Theory":         ["goal setting", "goal-setting"],
    "Social Cognitive Theory":     ["social cognitive", "self-efficacy", "bandura"],
    "Social Comparison Theory":    ["social comparison"],
    "Signaling Theory":            ["signaling theory", "signalling theory"],
    "Trust Theory":                ["trust theory", "trusting belief", "trustworthiness"],
    "Protection Motivation Theory":["protection motivation", "pmt"],
    "Privacy Calculus":            ["privacy calculus", "privacy concern"],
    "Diffusion of Innovations":    ["diffusion of innovation", "rogers", "innovation adoption"],
    "Elaboration Likelihood Model":["elm", "elaboration likelihood"],
    "Information Systems Success": ["delone", "mclean", "is success", "system quality", "information quality"],
    "Expectation-Confirmation":    ["expectation.confirmation", "ecm", "is continuance"],
    "Distributive Justice":        ["distributive justice", "fairness", "equity theory"],
}

_model      = None
_embeddings = None   # shape: (N, 768)  float32
_df         = None   # aligned row-by-row with _embeddings


def _load():
    global _model, _embeddings, _df

    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(FINETUNED_MODEL)

    if _embeddings is None or _df is None:
        if not os.path.exists(EMBEDDINGS_FILE):
            raise FileNotFoundError(
                f"Embeddings file not found: {EMBEDDINGS_FILE}\n"
                "Run the Colab notebook to generate embeddings first."
            )
        _embeddings = np.load(EMBEDDINGS_FILE).astype("float32")

        df = pd.read_csv(CLASSIFIED_CSV)
        if len(df) != _embeddings.shape[0]:
            raise ValueError(
                f"Row count mismatch: CSV has {len(df)} rows but "
                f"embeddings has {_embeddings.shape[0]} vectors."
            )
        _df = df


def _detect_theories(query: str) -> list[str]:
    """Return canonical theory names mentioned in the query."""
    q = query.lower()
    found = []
    for canonical, aliases in _THEORY_ALIASES.items():
        if any(re.search(alias, q) for alias in aliases):
            found.append(canonical)
    return found


def _behavioral_boost_array() -> np.ndarray:
    """Return per-paper behavioral boost as a numpy array."""
    boost = np.zeros(len(_df), dtype="float32")
    is_beh  = (_df["is_behavioral"] == True).values
    is_high = (_df["confidence"] == "high").values
    is_med  = (_df["confidence"] == "medium").values
    boost[is_beh & is_high] = BEHAVIORAL_BOOST
    boost[is_beh & is_med]  = BEHAVIORAL_BOOST * 0.5
    return boost


def _theory_match_array(detected_theories: list[str]) -> np.ndarray:
    """Return per-paper theory-match bonus based on detected theories in query."""
    if not detected_theories:
        return np.zeros(len(_df), dtype="float32")

    bonus = np.zeros(len(_df), dtype="float32")
    theories_col = _df["theories_used"].fillna("").str.lower().values

    for theory in detected_theories:
        keyword = theory.lower()
        matches = np.array([keyword in t for t in theories_col], dtype="float32")
        bonus += matches * THEORY_MATCH_BONUS

    return np.clip(bonus, 0, THEORY_MATCH_BONUS * 2)  # cap at 2 matched theories


def _native(val):
    """Convert numpy scalar types to native Python for JSON serialization."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return None
    if isinstance(val, np.integer):
        return int(val)
    if isinstance(val, np.floating):
        return float(val)
    if isinstance(val, np.bool_):
        return bool(val)
    return val


def search(
    query:           str,
    top_k:           int  = 10,
    only_behavioral: bool = False,
) -> list[dict]:
    """
    Encode query with SPECTER and return top_k papers by hybrid score.

    Args:
        query:           Natural language query from user.
        top_k:           Number of results to return (max 50).
        only_behavioral: If True, restrict results to behavioral papers only.

    Returns:
        List of dicts with paper fields + similarity + final_score.
    """
    _load()

    query_vec = _model.encode(query, convert_to_numpy=True).astype("float32")

    # ── Cosine similarity ──────────────────────────────────────────────────────
    paper_norms = np.linalg.norm(_embeddings, axis=1, keepdims=True)
    query_norm  = np.linalg.norm(query_vec)
    sim_scores  = (_embeddings / (paper_norms + 1e-9)) @ (query_vec / (query_norm + 1e-9))

    # ── Boost layers ───────────────────────────────────────────────────────────
    detected        = _detect_theories(query)
    beh_boost       = _behavioral_boost_array()
    theory_bonus    = _theory_match_array(detected)
    final_scores    = sim_scores + beh_boost + theory_bonus

    # ── Behavioral filter ──────────────────────────────────────────────────────
    if only_behavioral:
        mask         = (_df["is_behavioral"] == True).values
        final_scores = np.where(mask, final_scores, -1.0)

    top_indices = np.argsort(final_scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        row   = _df.iloc[idx]
        fscore = float(final_scores[idx])
        sscore = float(sim_scores[idx])
        if fscore < 0 and only_behavioral:
            break

        # matched_theories = theories detected in query AND present in this paper
        paper_theories = str(row.get("theories_used") or "").lower()
        matched = [t for t in detected if t.lower() in paper_theories] if detected else None

        results.append({
            "title":            _native(row.get("title")),
            "abstract":         _native(row.get("abstract")),
            "year":             _native(row.get("year")),
            "venue":            _native(row.get("venue")),
            "authors":          _native(row.get("authors")),
            "doi":              _native(row.get("doi")),
            "url":              _native(row.get("url")),
            "platform":         _native(row.get("platform")),
            "is_behavioral":    _native(row.get("is_behavioral")),
            "theories_used":    _native(row.get("theories_used")),
            "confidence":       _native(row.get("confidence")),
            "similarity":       round(sscore, 4),
            "score":            round(fscore, 4),
            "matched_theories": matched if matched else None,
        })

    return results
