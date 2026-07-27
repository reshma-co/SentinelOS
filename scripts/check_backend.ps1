$ErrorActionPreference = "Stop"

$Python = Join-Path $PSScriptRoot "..\backend\.venv\Scripts\python.exe"
& $Python -m pip --version
& $Python -c "import fastapi, uvicorn, requests, dotenv, pydantic, mcp; print('backend imports ok')"
