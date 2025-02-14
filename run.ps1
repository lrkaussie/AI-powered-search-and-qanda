# Start the FastAPI backend
$backend = Start-Process -FilePath "uvicorn" -ArgumentList "app.main:app --host 0.0.0.0 --port 8000" -PassThru

# Wait for the backend to start
Start-Sleep -Seconds 5

# Start the Streamlit frontend
Set-Location frontend
streamlit run app.py --server.port 8501

# Clean up the backend process when done
Stop-Process -Id $backend.Id 