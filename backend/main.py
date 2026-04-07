"""
backend/main.py — FastAPI application entry point
To start (run from the backend/ directory):
    PYTHONPATH=. uvicorn main:app --reload
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import papers, stats, jobs, search

app = FastAPI(title="LitScope API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(papers.router)
app.include_router(stats.router)
app.include_router(jobs.router)
app.include_router(search.router)

frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")


@app.get("/api/health")
def health():
    return {"status": "ok"}
