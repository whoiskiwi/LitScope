"""
scripts/classify_all.py — Classify unclassified papers, no fetching
Usage: python scripts/classify_all.py [--input ...] [--output ...]
"""

import argparse

from litscope.config     import CLASSIFIED_CSV
from litscope.classifier import classify_dataframe
from litscope.organizer  import sort_by_platform_and_year, print_summary
from litscope.storage    import load_csv, save_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default=CLASSIFIED_CSV)
    parser.add_argument("--output", default=CLASSIFIED_CSV)
    args = parser.parse_args()

    df = load_csv(args.input)
    print(f"Total: {len(df)} papers, pending classification: {df['is_behavioral'].isna().sum()}\n")

    if df["is_behavioral"].isna().sum() == 0:
        print("All papers are already classified.")
        return

    df = classify_dataframe(df, autosave_path=args.output)
    df = sort_by_platform_and_year(df)
    save_csv(df, args.output)
    print_summary(df)


if __name__ == "__main__":
    main()
