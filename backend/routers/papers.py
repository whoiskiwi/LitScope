"""
routers/papers.py — Read-only paper data endpoints
"""

from urllib.parse import unquote
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from litscope.config  import CLASSIFIED_CSV
from litscope.storage import load_csv

router = APIRouter(prefix="/api/papers", tags=["papers"])


def _load():
    return load_csv(CLASSIFIED_CSV)


@router.get("")
def list_papers(
    platform:      Optional[str]  = Query(None),
    year_min:      Optional[int]  = Query(None),
    year_max:      Optional[int]  = Query(None),
    is_behavioral: Optional[bool] = Query(None),
    keyword:       Optional[str]  = Query(None),
    page:          int            = Query(1, ge=1),
    page_size:     int            = Query(50, ge=1, le=200),
):
    df = _load()

    if platform:
        df = df[df["platform"] == platform]
    if year_min is not None:
        df = df[df["year"] >= year_min]
    if year_max is not None:
        df = df[df["year"] <= year_max]
    if is_behavioral is not None:
        df = df[df["is_behavioral"] == is_behavioral]
    if keyword:
        kw = keyword.lower()
        mask = (
            df["title"].str.lower().str.contains(kw, na=False) |
            df["abstract"].str.lower().str.contains(kw, na=False)
        )
        df = df[mask]

    total   = len(df)
    offset  = (page - 1) * page_size
    page_df = df.iloc[offset: offset + page_size]

    return {
        "total":     total,
        "page":      page,
        "page_size": page_size,
        "data":      page_df.where(page_df.notna(), None).to_dict(orient="records"),
    }


@router.get("/{doi_encoded}")
def get_paper(doi_encoded: str):
    doi   = unquote(doi_encoded).lower().strip()
    df    = _load()
    match = df[df["doi"].str.lower().str.strip() == doi]
    if match.empty:
        raise HTTPException(status_code=404, detail="Paper not found")
    row = match.iloc[0]
    return row.where(row.notna(), None).to_dict()
