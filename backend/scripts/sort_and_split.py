"""
scripts/sort_and_split.py — Sort and split by platform, no fetching or classification
Usage: python scripts/sort_and_split.py
"""

from litscope.config    import CLASSIFIED_CSV, BY_PLATFORM_CSV, BY_PLATFORM_DIR
from litscope.organizer import sort_by_platform_and_year, split_by_platform, print_summary, tag_platform
from litscope.storage   import load_csv, save_csv


def main():
    df = load_csv(CLASSIFIED_CSV)
    print(f"Total: {len(df)} papers")

    df = tag_platform(df)
    df = sort_by_platform_and_year(df)
    save_csv(df, BY_PLATFORM_CSV)
    split_by_platform(df, BY_PLATFORM_DIR)
    print_summary(df)


if __name__ == "__main__":
    main()
