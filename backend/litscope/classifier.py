"""
classifier.py — Paper classification, handles only DeepSeek API calls, no fetching
"""

import json
import time
import requests
from litscope.config import DEEPSEEK_API_KEY

_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Reference list of behavioral/psychological theories commonly used in IS research.
BEHAVIORAL_THEORIES = [
    "Technology Acceptance Model (TAM)",
    "Theory of Planned Behavior (TPB)",
    "Theory of Reasoned Action (TRA)",
    "UTAUT / UTAUT2",
    "Prospect Theory",
    "Bounded Rationality",
    "Mental Accounting",
    "Framing Effects",
    "Anchoring and Adjustment",
    "Self-Determination Theory (SDT)",
    "Regulatory Focus Theory",
    "Goal-Setting Theory",
    "Social Cognitive Theory",
    "Social Comparison Theory",
    "Signaling Theory",
    "Trust Theory",
    "Protection Motivation Theory",
    "Privacy Calculus",
    "Diffusion of Innovations",
]

_PROMPT_TEMPLATE = """You are an expert in Information Systems research.
Analyze the following academic paper and determine if it uses any behavioral or psychological theory.

Paper Title: {title}
Abstract: {abstract}

Common behavioral/psychological theories in IS research include (but are not limited to):
{theories}

Answer in JSON format only, no other text:
{{
  "is_behavioral": true or false,
  "theories_used": ["theory1", "theory2"],
  "confidence": "high" or "medium" or "low",
  "reason": "one sentence explanation"
}}

Rules:
- is_behavioral = true only if the paper explicitly uses a behavioral/psychological theory as its theoretical foundation
- theories_used = list the specific theories found, use standard names (not limited to the list above)
- If no behavioral theory is used, theories_used = []
"""


def classify_paper(title: str, abstract: str) -> dict:
    prompt = _PROMPT_TEMPLATE.format(
        title=title,
        abstract=abstract,
        theories="\n".join(f"- {t}" for t in BEHAVIORAL_THEORIES),
    )
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type":  "application/json",
    }
    body = {
        "model":       "deepseek-chat",
        "messages":    [{"role": "user", "content": prompt}],
        "max_tokens":  400,
        "temperature": 0.1,
    }
    try:
        r = requests.post(_API_URL, headers=headers, json=body, timeout=30)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        content = content.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        return {
            "is_behavioral": None,
            "theories_used": [],
            "confidence":    "low",
            "reason":        f"Error: {e}",
        }


def classify_dataframe(df, delay: float = 0.5, autosave_path: str = None, autosave_every: int = 10):
    """
    Classify all unclassified rows in df (where is_behavioral is NaN).

    Args:
        df:             DataFrame with title / abstract / is_behavioral columns
        delay:          Seconds to wait between API calls
        autosave_path:  If provided, saves progress to this CSV every `autosave_every` papers
        autosave_every: How often to auto-save (default: every 10 papers)
    """
    mask  = df["is_behavioral"].isna()
    total = mask.sum()
    print(f"[Classifier] Pending classification: {total} papers\n")

    for i, idx in enumerate(df[mask].index):
        title    = str(df.at[idx, "title"])
        abstract = str(df.at[idx, "abstract"])

        if len(abstract) < 50 or any(kw in title for kw in ("Special Section", "Call for Papers")):
            df.at[idx, "is_behavioral"] = False
            df.at[idx, "theories_used"] = ""
            df.at[idx, "confidence"]    = "high"
            df.at[idx, "reason"]        = "Not a research paper (editorial/announcement)"
            print(f"  [{i+1}/{total}] Skipped (not a research paper): {title[:60]}")
            continue

        print(f"  [{i+1}/{total}] Classifying: {title[:65]}...")
        result = classify_paper(title, abstract)

        df.at[idx, "is_behavioral"] = result.get("is_behavioral")
        df.at[idx, "theories_used"] = ", ".join(result.get("theories_used", []))
        df.at[idx, "confidence"]    = result.get("confidence")
        df.at[idx, "reason"]        = result.get("reason")

        tag = "✅" if result.get("is_behavioral") else "❌"
        print(f"    {tag} {df.at[idx, 'theories_used'] or '—'}")

        if autosave_path and (i + 1) % autosave_every == 0:
            df.to_csv(autosave_path, index=False, encoding="utf-8-sig")
            print(f"  ── Auto-saved ({i+1}/{total}) ──")

        time.sleep(delay)

    return df
