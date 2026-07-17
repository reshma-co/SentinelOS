# NitroStack Hackathon Workspace

This workspace is prepared for building AI applications with Python, FastAPI, Git, GitHub, MCP, LLM APIs, and optional Node.js tooling.

## Structure

- `backend/` - FastAPI backend and Python virtual environment.
- `frontend/` - Optional web UI or Node.js frontend.
- `agents/` - Starter agent code and shared agent utilities.
- `mcp/` - Sample MCP server and client.
- `data/` - Local datasets and temporary files. Contents are ignored by Git.
- `docs/` - Notes, architecture docs, prompts, and hackathon planning.
- `scripts/` - Automation scripts for setup, demos, and checks.
- `tests/` - Test files.

## Backend Quick Start

From PowerShell:

```powershell
cd .\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Then open:

- API root: `http://127.0.0.1:8000/`
- Health check: `http://127.0.0.1:8000/health`
- Swagger docs: `http://127.0.0.1:8000/docs`

If PowerShell blocks activation scripts, use this instead:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

## Environment Variables

Copy `.env.example` to `.env` and fill in local secrets as needed. Do not commit `.env`.

## MCP Samples

The `mcp/` folder contains a minimal server and client using the Python MCP SDK. Run them after activating the backend virtual environment.

```powershell
cd .\mcp
..\\backend\\.venv\\Scripts\\python.exe sample_client.py
```

## Recommended Tools

- Visual Studio Code
- Python extension
- Pylance
- Ruff
- GitHub Pull Requests and Issues
- GitHub Copilot, if your team uses it
