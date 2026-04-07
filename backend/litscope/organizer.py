"""
organizer.py — Data organization: merging, deduplication, sorting, platform tagging, and platform splitting
No network requests, no classification
"""

import os
import pandas as pd
from litscope.config import VENUE_PLATFORM_MAP, PLATFORM_ORDER


def get_platform(venue: str, fallback: str = "Unknown") -> str:
    for key, platform in VENUE_PLATFORM_MAP.items():
        if key.lower() in str(venue).lower():
            return platform
    return fallback


def tag_platform(df: pd.DataFrame) -> pd.DataFrame:
    df["platform"] = df.apply(
        lambda r: get_platform(r.get("venue", ""), r.get("source", "Unknown")),
        axis=1,
    )
    return df


def merge_and_dedup(df_existing: pd.DataFrame, df_new: pd.DataFrame) -> pd.DataFrame:
    for col in df_existing.columns:
        if col not in df_new.columns:
            df_new[col] = None
    df_new = df_new[df_existing.columns]
    df_all = pd.concat([df_existing, df_new], ignore_index=True)
    df_all.drop_duplicates(subset=["doi"], keep="first", inplace=True)
    return df_all


def sort_by_platform_and_year(df: pd.DataFrame) -> pd.DataFrame:
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    order_map  = {p: i for i, p in enumerate(PLATFORM_ORDER)}
    df["_order"] = df["platform"].map(order_map).fillna(len(PLATFORM_ORDER))
    df.sort_values(["_order", "year"], ascending=[True, False], inplace=True, na_position="last")
    df.drop(columns=["_order"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def split_by_platform(df: pd.DataFrame, out_dir: str) -> None:
    """
    Save one CSV per platform.

    Output structure:
        by_platform/
        ├── INFORMS_-_ISR.csv
        ├── AIS_-_MISQ.csv
        └── Taylor_&_Francis_-_JMIS.csv
    """
    os.makedirs(out_dir, exist_ok=True)

    for platform in PLATFORM_ORDER:
        sub = df[df["platform"] == platform].copy()
        if sub.empty:
            continue
        safe_name = platform.replace("/", "-").replace(" ", "_")
        sub.to_csv(os.path.join(out_dir, f"{safe_name}.csv"), index=False, encoding="utf-8-sig")



def print_summary(df: pd.DataFrame) -> None:
    print(f"\n{'='*55}")
    print(f"  {'Platform':<26} {'Total':>6} {'Behavioral':>10} {'Year Range':>12}")
    print(f"  {'-'*53}")
    for p in PLATFORM_ORDER:
        sub = df[df["platform"] == p]
        if sub.empty:
            continue
        b  = int((sub["is_behavioral"] == True).sum())
        yr = (f"{int(sub['year'].min())}–{int(sub['year'].max())}"
              if sub["year"].notna().any() else "N/A")
        print(f"  {p:<26} {len(sub):>6} {b:>10} {yr:>12}")
    print(f"{'='*55}")
    print(f"  {'Total':<26} {len(df):>6}")
