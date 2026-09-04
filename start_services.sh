#!/usr/bin/env bash
set -e

echo "==> Cleaning up any lingering processes on ports 8001 and 8090..."
fuser -k 8001/tcp 2>/dev/null || true
fuser -k 8090/tcp 2>/dev/null || true
pkill -f "uvicorn q_shield.api.main:app" || true
pkill -f "http.server 8090" || true
sleep 1

echo "==> Starting Q-Shield FastAPI Backend on port 8001..."
PYTHONPATH=. uvicorn q_shield.api.main:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

echo "==> Starting Frontend Dashboard on port 8090..."
python3 -m http.server 8090 --directory frontend &
FRONTEND_PID=$!

echo ""
echo "===================================================="
echo " Q-Shield ECDAT Services Active!"
echo " - Dashboard: http://127.0.0.1:8090"
echo " - API Docs:  http://127.0.0.1:8001/docs"
echo "===================================================="
echo ""

# Trap exit to kill background jobs cleanly
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
