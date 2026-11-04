# Backend

FastAPI service for the self-healing tool (Railway).

```bash
uv venv --clear .venv && uv pip install -p .venv -r requirements-dev.txt
.venv/bin/pytest
.venv/bin/uvicorn app.main:app --reload --port 8001
```

Implemented: `GET /health`, `POST /webhooks/sentry` (verifies `Sentry-Hook-Signature`, extracts the issue).
Next: store issues in Neon, group duplicates, trigger the GitHub Action.
