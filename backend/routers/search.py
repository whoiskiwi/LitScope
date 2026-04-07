"""
routers/search.py — Semantic search endpoint
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from litscope.searcher import search

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
