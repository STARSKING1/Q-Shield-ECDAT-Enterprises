#!/usr/bin/env bash
set -e

echo "==> Installing required Python dependencies..."
pip install --no-cache-dir fastapi uvicorn pydantic libcst click httpx pytest

echo "==> Running verification test suite..."
PYTHONPATH=. pytest tests/ -v

echo "==> Launching FastAPI backend on port 8001..."
PYTHONPATH=. uvicorn q_shield.api.main:app --host 0.0.0.0 --port 8001 --reload
