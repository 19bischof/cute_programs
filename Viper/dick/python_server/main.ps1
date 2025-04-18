Start-Process "venv\Scripts\uvicorn.exe" `
  -ArgumentList "app:app --host 127.0.0.1 --port 8000" `
  -RedirectStandardOutput "uvicorn.log" `
  -RedirectStandardError "uvicorn_error.log"
