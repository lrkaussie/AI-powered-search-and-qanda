@echo off

:: Start the FastAPI backend
start /B uvicorn app.main:app --host 0.0.0.0 --port 8000

:: Wait for the backend to start
timeout /t 5 /nobreak

:: Start the Streamlit frontend
cd frontend && streamlit run app.py --server.port 8501

:: Note: Process cleanup will need to be done manually in Windows
:: You can use Task Manager or `taskkill` to stop the uvicorn process 