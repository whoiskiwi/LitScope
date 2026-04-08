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

    # Normalize theory name variants to canonical names before counting
    _CANON = {
        # TAM
        "tam":                                                   "Technology Acceptance Model (TAM)",
        "technology acceptance model":                           "Technology Acceptance Model (TAM)",
        "technology acceptance model (tam)":                     "Technology Acceptance Model (TAM)",
        "technology acceptance model (implied)":                 "Technology Acceptance Model (TAM)",
        "technology acceptance theories":                        "Technology Acceptance Model (TAM)",
        # UTAUT
        "utaut":                                                 "UTAUT",
        "utaut2":                                                "UTAUT",
        "unified theory of acceptance and use of technology":    "UTAUT",
        "unified theory of acceptance and use of technology (utaut)": "UTAUT",
        # TPB
        "theory of planned behavior":                            "Theory of Planned Behavior (TPB)",
        "theory of planned behavior (tpb)":                      "Theory of Planned Behavior (TPB)",
        "theory of planned behaviour":                           "Theory of Planned Behavior (TPB)",
        # TRA
        "theory of reasoned action":                             "Theory of Reasoned Action (TRA)",
        "theory of reasoned action (tra)":                       "Theory of Reasoned Action (TRA)",
        # SDT
        "self-determination theory":                             "Self-Determination Theory (SDT)",
        "self-determination theory (sdt)":                       "Self-Determination Theory (SDT)",
        # PMT
        "protection motivation theory":                          "Protection Motivation Theory (PMT)",
        "protection motivation theory (pmt)":                    "Protection Motivation Theory (PMT)",
        # Casing fixes
        "coping theory":                                         "Coping Theory",
        "social cognitive theory":                               "Social Cognitive Theory",
        "social comparison theory":                              "Social Comparison Theory",
        "social capital theory":                                 "Social Capital Theory",
        "social exchange theory":                                "Social Exchange Theory",
        "social presence theory":                                "Social Presence Theory",
        "signaling theory":                                      "Signaling Theory",
        "trust theory":                                          "Trust Theory",
        "privacy calculus":                                      "Privacy Calculus",
        "prospect theory":                                       "Prospect Theory",
        "framing effects":                                       "Framing Effects",
        "bounded rationality":                                   "Bounded Rationality",
        "goal-setting theory":                                   "Goal-Setting Theory",
        "anchoring and adjustment":                              "Anchoring and Adjustment",
        "elaboration likelihood model":                          "Elaboration Likelihood Model (ELM)",
        "elaboration likelihood model (elm)":                    "Elaboration Likelihood Model (ELM)",
        "innovation diffusion theory":                           "Innovation Diffusion Theory",
        "diffusion of innovations":                              "Innovation Diffusion Theory",
        "media richness theory":                                 "Media Richness Theory",
        "flow theory":                                           "Flow Theory",
    }

    def _canonicalize(name: str) -> str:
        return _CANON.get(name.strip().lower(), name.strip())

    theories = (
        df["theories_used"].dropna()
        .str.split(", ").explode()
        .str.strip().replace("", None).dropna()
        .apply(_canonicalize)
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
