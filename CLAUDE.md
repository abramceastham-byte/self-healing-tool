# Self-Healing Tool

A class project. It plugs into a GitHub repo, catches production errors with Sentry, has an AI agent (Claude Code or Codex in a GitHub Action) write a failing test and a fix, opens a PR with a plain-language summary, deploys the fix, rolls back if errors rise, and notifies the user on Discord, Slack, or email.

## Architecture
- **Backend** (Python + FastAPI, Railway): receives Sentry webhooks, groups duplicate errors, triggers the GitHub Action, watches error rates after deploys, reverts bad fixes, sends notifications.
- **Database** (Neon PostgreSQL): errors, fix attempts, test results, deploys, rollbacks, and a per-repo "fix memory" fed to the agent as context.
- **Dashboard** (React, Vercel).
- **Agent**: Claude Code or Codex running in GitHub Actions.
- **Per connected repo**: `.selfheal/config.yml` (auto-deploy vs approval, max attempts per bug, protected files, notification channel), `.selfheal/rules.md` (notes for the agent), and one workflow file.
- Everything must stay on free tiers.

## Layout
- `backend/` FastAPI service (webhook endpoint started)
- `dashboard/` React app (not built yet)
- `demo-app/` product-reviews FastAPI app with a planted bug; the tool's test target. It is a git submodule (own repo `selfheal-demo-app`). Commit inside it, then commit the updated pointer here.
- `docs/` project docs; `docs/planted-bugs.md` is the answer key. Do not read it when acting as the fixing agent.
- `.selfheal/` example config, rules, and workflow for a connected repo

## Run and test
- Demo app: `cd demo-app && uv venv --clear .venv && uv pip install -p .venv -r requirements-dev.txt && .venv/bin/uvicorn app.main:app --reload`; tests: `.venv/bin/pytest`
- Backend: `cd backend && uv venv --clear .venv && uv pip install -p .venv -r requirements-dev.txt`; run: `.venv/bin/uvicorn app.main:app --reload --port 8001`; tests: `.venv/bin/pytest`
- Dashboard: not built yet (will be `npm test` in `dashboard/`)

## Rules
1. Write tests before fixes: reproduce with a failing test, then fix.
2. Keep changes small and focused.
3. Never edit files listed under `protected_files` in `.selfheal/config.yml`.
4. Never commit secrets. Use environment variables and keep `.env.example` current.
5. Commit messages are imperative and cover one idea, e.g. "Add webhook endpoint".
