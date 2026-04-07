"""
storage.py — CSV read/write, the single place handling encoding and column order
"""

import pandas as pd
from litscope.config import CSV_COLUMNS


def load_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=CSV_COLUMNS)
    df["year"] = pd.to_numeric(df.get("year"), errors="coerce")
    return df


def save_csv(df: pd.DataFrame, path: str) -> None:
    for col in CSV_COLUMNS:
        if col not in df.columns:
            df[col] = None
    df = df[CSV_COLUMNS]
    df.to_csv(path, index=False, encoding="utf-8-sig")


def get_existing_dois(df: pd.DataFrame) -> set:
    return set(df["doi"].dropna().str.strip().str.lower())
