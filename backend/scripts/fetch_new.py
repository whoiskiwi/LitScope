"""
scripts/fetch_new.py — Fetch papers, no classification
Usage: python scripts/fetch_new.py [--journals ISR MISQ JMIS]
"""

import argparse
import pandas as pd

from litscope.config    import JOURNALS, CLASSIFIED_CSV, RAW_CSV
from litscope.fetcher   import fetch_openalex
from litscope.storage   import load_csv, save_csv, get_existing_dois
from litscope.organizer import merge_and_dedup, sort_by_platform_and_year, print_summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--journals", nargs="*")
    args = parser.parse_args()

    if args.journals:
        shorts   = [j.upper() for j in args.journals]
        journals = [j for j in JOURNALS if j["short"] in shorts]
    else:
        journals = JOURNALS

    df_existing  = load_csv(CLASSIFIED_CSV)
    exclude_dois = get_existing_dois(df_existing)
    print(f"Existing papers: {len(df_existing)}, known DOIs: {len(exclude_dois)}\n")

    all_new = []
    for journal in journals:
        papers = fetch_openalex(journal, exclude_dois=exclude_dois)
        all_new.extend(papers)

    print(f"\nTotal new papers: {len(all_new)}")
    if not all_new:
        return

    df_new    = pd.DataFrame(all_new)
    save_csv(df_new, RAW_CSV)

    df_merged = merge_and_dedup(df_existing, df_new)
    df_merged = sort_by_platform_and_year(df_merged)
    save_csv(df_merged, CLASSIFIED_CSV)
    print_summary(df_merged)


if __name__ == "__main__":
    main()
