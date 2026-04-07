"""
routers/stats.py — Statistics data endpoints
"""

from fastapi import APIRouter
from litscope.config  import CLASSIFIED_CSV
from litscope.storage import load_csv

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("")
def get_stats():
    df = load_csv(CLASSIFIED_CSV)

    total        = len(df)
    behavioral   = int((df["is_behavioral"] == True).sum())
    unclassified = int(df["is_behavioral"].isna().sum())

    by_platform = []
    for platform, group in df.groupby("platform", dropna=False):
        by_platform.append({
            "platform":   platform,
            "total":      len(group),
            "behavioral": int((group["is_behavioral"] == True).sum()),
        })

    year_counts = (
        df["year"].dropna().astype(int)
        .value_counts().sort_index()
        .rename_axis("year").reset_index(name="count")
    )
    by_year = year_counts.to_dict(orient="records")

    theories = (
        df["theories_used"].dropna()
        .str.split(", ").explode()
        .str.strip().replace("", None).dropna()
        .value_counts().head(10)
        .rename_axis("theory").reset_index(name="count")
    )
    top_theories = theories.to_dict(orient="records")

    return {
        "total":            total,
        "behavioral_count": behavioral,
        "behavioral_pct":   round(behavioral / total * 100, 1) if total else 0,
        "unclassified":     unclassified,
        "by_platform":      by_platform,
        "by_year":          by_year,
        "top_theories":     top_theories,
    }
