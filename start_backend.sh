#!/bin/bash
cd "$(dirname "$0")/backend"
PYTHONPATH=. uvicorn main:app --reload
