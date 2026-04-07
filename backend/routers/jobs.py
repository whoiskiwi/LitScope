"""
routers/jobs.py — Job trigger and status query endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from services import job_runner

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


class FetchRequest(BaseModel):
    journals: Optional[list[str]] = None


@router.post("/fetch")
def trigger_fetch(body: FetchRequest = FetchRequest()):
    job_id = job_runner.run_fetch(body.journals)
    if job_id is None:
        raise HTTPException(status_code=409, detail="fetch job is already running")
    return {"job_id": job_id, "job_type": "fetch", "status": "running"}


@router.post("/classify")
def trigger_classify():
    job_id = job_runner.run_classify()
    if job_id is None:
        raise HTTPException(status_code=409, detail="classify job is already running")
    return {"job_id": job_id, "job_type": "classify", "status": "running"}


@router.post("/sort")
def trigger_sort():
    job_id = job_runner.run_sort()
    if job_id is None:
        raise HTTPException(status_code=409, detail="sort job is already running")
    return {"job_id": job_id, "job_type": "sort", "status": "running"}


@router.get("")
def list_jobs():
    jobs = job_runner.get_all_jobs()
    return [_serialize(s) for s in jobs.values()]


@router.get("/{job_type}")
def get_job(job_type: str):
    state = job_runner.get_job(job_type)
    if state is None:
        raise HTTPException(status_code=404, detail="No job record found for this type")
    return _serialize(state)


def _serialize(state) -> dict:
    return {
        "job_id":      state.job_id,
        "job_type":    state.job_type,
        "status":      state.status,
        "started_at":  state.started_at,
        "finished_at": state.finished_at,
        "log":         state.log,
        "result":      state.result,
    }
