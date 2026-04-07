"""
fetcher.py — Paper fetching, handles only network requests, no classification
"""

import time
import requests
from litscope.config import OPENALEX_USER_AGENT, FETCH_BATCH


def _reconstruct_abstract(inverted_index: dict) -> str:
    if not inverted_index:
        return ""
    words = {pos: word for word, positions in inverted_index.items() for pos in positions}
    return " ".join(words[i] for i in sorted(words))


def fetch_openalex(journal: dict, exclude_dois: set = None) -> list:
    exclude_dois = exclude_dois or set()
    papers  = []
    url     = "https://api.openalex.org/works"
    headers = {"User-Agent": OPENALEX_USER_AGENT}
    params  = {
        "filter":   f"primary_location.source.id:{journal['openalex_id']},has_abstract:true",
        "select":   "title,abstract_inverted_index,publication_year,doi,authorships",
        "per-page": FETCH_BATCH,
        "page":     1,
        "sort":     "publication_year:desc",
    }

    print(f"[Fetcher] {journal['short']} — fetching up to {journal['max']} papers")

    while len(papers) < journal["max"]:
        try:
            r = requests.get(url, headers=headers, params=params, timeout=20)
            if r.status_code != 200:
                print(f"  HTTP {r.status_code}, stopping")
                break

            items = r.json().get("results", [])
            if not items:
                print("  No more data")
                break

            for item in items:
                abstract = _reconstruct_abstract(item.get("abstract_inverted_index") or {})
                if not abstract:
                    continue

                raw_doi = (item.get("doi") or "").strip()
                doi     = raw_doi.replace("https://doi.org/", "").lower()  # clean identifier only
                if doi in exclude_dois:
                    continue

                authors = [
                    a["author"]["display_name"]
                    for a in item.get("authorships", [])
                    if a.get("author")
                ]

                papers.append({
                    "title":    item.get("title"),
                    "abstract": abstract,
                    "year":     item.get("publication_year"),
                    "venue":    journal["name"],
                    "authors":  ", ".join(authors),
                    "doi":      doi,                                        # e.g. 10.1287/isre.xxx
                    "url":      f"https://doi.org/{doi}" if doi else "",   # full clickable URL
                    "source":   "OpenAlex",
                    "platform": journal["platform"],
                })

                if doi:
                    exclude_dois.add(doi)

            print(f"  Fetched {len(papers)} papers (page {params['page']})")
            params["page"] += 1
            time.sleep(1)

        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(5)

    print(f"  Done, total {len(papers)} papers\n")
    return papers
