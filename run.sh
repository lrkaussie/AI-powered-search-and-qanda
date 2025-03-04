#!/bin/bash

# Start the FastAPI backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for the backend to start
sleep 5

# Start the Streamlit frontend
cd frontend && streamlit run app.py --server.port 8501

# If frontend exits, kill the backend
kill $BACKEND_PID
