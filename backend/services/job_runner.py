"""
services/job_runner.py
======================
Runs long-running tasks (fetch/classify/sort) in background threads without blocking the FastAPI event loop.
"""

import sys
import uuid
import threading
from io import StringIO
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class JobState:
    job_id:      str
    job_type:    str
    status:      str = "running"
    started_at:  str = ""
    finished_at: str = ""
    log:         list = field(default_factory=list)
    result:      str = ""


_jobs:  dict[str, JobState] = {}
_locks: dict[str, threading.Lock] = {
    "fetch":    threading.Lock(),
    "classify": threading.Lock(),
    "sort":     threading.Lock(),
}


def _run_in_thread(job_type: str, target_fn, *args):
    if not _locks[job_type].acquire(blocking=False):
        return None

    job_id = str(uuid.uuid4())[:8]
    state  = JobState(
        job_id     = job_id,
        job_type   = job_type,
        started_at = datetime.now().isoformat(timespec="seconds"),
    )
    _jobs[job_type] = state

    def run():
        buf = StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            result = target_fn(*args)
            state.result = str(result or "Done")
            state.status = "done"
        except Exception as e:
            state.result = f"Error: {e}"
            state.status = "error"
        finally:
            sys.stdout = old_stdout
            state.log = buf.getvalue().splitlines()
            state.finished_at = datetime.now().isoformat(timespec="seconds")
            _locks[job_type].release()

    threading.Thread(target=run, daemon=True).start()
    return job_id


def run_fetch(journals: list[str] | None = None) -> Optional[str]:
    from litscope.config    import JOURNALS, CLASSIFIED_CSV, RAW_CSV
    from litscope.fetcher   import fetch_openalex
    from litscope.storage   import load_csv, save_csv, get_existing_dois
    from litscope.organizer import merge_and_dedup, sort_by_platform_and_year
    import pandas as pd

    def _fetch():
        targets      = JOURNALS if not journals else [j for j in JOURNALS if j["short"] in journals]
        df_existing  = load_csv(CLASSIFIED_CSV)
        exclude_dois = get_existing_dois(df_existing)
        all_new = []
        for j in targets:
            papers = fetch_openalex(j, exclude_dois=exclude_dois)
            all_new.extend(papers)
        if all_new:
            df_new    = pd.DataFrame(all_new)
            save_csv(df_new, RAW_CSV)
            df_merged = merge_and_dedup(df_existing, df_new)
            df_merged = sort_by_platform_and_year(df_merged)
            save_csv(df_merged, CLASSIFIED_CSV)
        return f"Added {len(all_new)} new papers"

    return _run_in_thread("fetch", _fetch)


def run_classify() -> Optional[str]:
    from litscope.config     import CLASSIFIED_CSV
    from litscope.classifier import classify_dataframe
    from litscope.organizer  import sort_by_platform_and_year
    from litscope.storage    import load_csv, save_csv

    def _classify():
        df = load_csv(CLASSIFIED_CSV)
        df = classify_dataframe(df, autosave_path=CLASSIFIED_CSV)
        df = sort_by_platform_and_year(df)
        save_csv(df, CLASSIFIED_CSV)
        return f"Classification complete, behavioral: {(df['is_behavioral'] == True).sum()}"

    return _run_in_thread("classify", _classify)


def run_sort() -> Optional[str]:
    from litscope.config    import CLASSIFIED_CSV, BY_PLATFORM_CSV, BY_PLATFORM_DIR
    from litscope.organizer import sort_by_platform_and_year, split_by_platform, tag_platform
    from litscope.storage   import load_csv, save_csv

    def _sort():
        df = load_csv(CLASSIFIED_CSV)
        df = tag_platform(df)
        df = sort_by_platform_and_year(df)
        save_csv(df, BY_PLATFORM_CSV)
        split_by_platform(df, BY_PLATFORM_DIR)
        return f"Sorted {len(df)} papers"

    return _run_in_thread("sort", _sort)


def get_job(job_type: str) -> Optional[JobState]:
    return _jobs.get(job_type)


def get_all_jobs() -> dict:
    return {k: v for k, v in _jobs.items()}
