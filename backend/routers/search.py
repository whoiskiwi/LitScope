"""
routers/search.py — Semantic search endpoint
"""

import random
import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from litscope.searcher import search
from litscope.config import CLASSIFIED_CSV

router = APIRouter(prefix="/api/search", tags=["search"])


class SearchRequest(BaseModel):
    query:           str
    top_k:           int  = 10
    only_behavioral: bool = False


@router.post("")
def semantic_search(req: SearchRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    if req.top_k < 1 or req.top_k > 50:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")

    results = search(
        query=req.query.strip(),
        top_k=req.top_k,
        only_behavioral=req.only_behavioral,
    )
    return {"query": req.query, "results": results}


@router.get("/examples")
def get_example_queries(n: int = Query(6, ge=1, le=20)):
    """
    Sample behavioral papers, use their titles as queries, run real search,
    return the n queries with highest top-1 similarity (what the model is best at).
    """
    df = pd.read_csv(CLASSIFIED_CSV)
    pool = df[(df["is_behavioral"] == True) & (df["confidence"] == "high")]["title"].dropna()
    candidates = pool.sample(min(20, len(pool)), random_state=random.randint(0, 9999)).tolist()

    scored = []
    for title in candidates:
        try:
            results = search(query=title, top_k=1)
            if results:
                scored.append({"query": title, "similarity": results[0]["similarity"]})
        except Exception:
            pass

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return {"examples": [s["query"] for s in scored[:n]]}


@router.get("")
def semantic_search_get(
    q:               str           = Query(..., description="Natural language query"),
    top_k:           int           = Query(10, ge=1, le=50),
    only_behavioral: bool          = Query(False),
):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    results = search(query=q.strip(), top_k=top_k, only_behavioral=only_behavioral)
    return {"query": q, "results": results}
