# Prototype submission

## 1. Summary
The self-healing tool plugs into a GitHub repo, catches production errors with Sentry, and has an AI agent write a failing test and a fix. It then opens a pull request with a plain-language summary. The full design also deploys the fix, rolls it back if errors rise, and notifies the user on Discord, Slack, or email. Everything runs on free tiers.

**What the prototype does today**
- `demo-app/`: a FastAPI + SQLite product-reviews app with one planted bug (average rating crashes with `ZeroDivisionError` for a product with no reviews). 13 passing tests. Sentry setup reads `SENTRY_DSN` and does nothing if missing.
- `backend/`: FastAPI service with `POST /webhooks/sentry` that verifies Sentry's HMAC signature and extracts the issue. 6 passing tests.
- Agent workflow (`demo-app/.github/workflows/self-heal.yml`): given an error, Gemini CLI writes a failing test and a fix, a guard script blocks protected-file edits and fixes with no test, `pytest` runs, and a PR is opened.
- Result: the first automated PR (#1 in the demo-app repo) added an empty-list check and a test. It passed.

**Limitation to state honestly:** the error details for that run were typed in by hand. Sentry-to-backend-to-workflow is not connected yet.

## 2. Repo URLs
- Main project: https://github.com/abramceastham-byte/self-healing-tool (includes `demo-app/` as a submodule)
- Demo app: https://github.com/abramceastham-byte/selfheal-demo-app
- Both are private; `drchangliu` is invited.

## 3. Prompts (summary)
1. One large prompt describing the project and architecture, asking for (a) a skeleton with `CLAUDE.md` and README (with an "AI Use" section) and (b) the demo app with a planted bug that the tests do not cover and no hint comments in the code.
2. Asked how the tool would detect the planted bug; Claude explained the Sentry-to-agent flow and its limits.
3. Asked for the backend; Claude wrote tests first for the Sentry webhook endpoint, then the code.
4. Asked what is the minimum for an end-to-end demo; chose Gemini's free key instead of a paid one.
5. Asked Claude to build the GitHub workflow, create the repo, and set the secret. Debugged failures from the logs: untrusted workspace, then Gemini 503 overload, then switched model after checking AI Studio's rate-limit page.

## 4. Screenshots to take
- Demo app showing the 500 / "Could not load rating" for Desk Lamp
- `pytest` passing in `demo-app` and `backend`
- GitHub Actions list: failed runs, then the green Self-heal run
- PR #1: description and "Files changed"
- AI Studio rate-limit page (shows free tier use)
- Folder tree in VS Code

## 5. Next steps
1. Connect Sentry: capture the demo app's crash, inspect a real webhook payload.
2. Backend triggers the Self-heal workflow via `workflow_dispatch`, with in-memory dedupe.
3. Deploy the demo app and backend to Railway; merging the PR auto-deploys.
4. Discord notification with the PR link.
5. Neon database for errors, attempts, and deploys; fix memory.
6. Rollback when the error rate rises after a deploy.
7. React dashboard on Vercel; Slack and email channels.

## 6. LLMs used (facts to base your reflection on; write the reflection yourself)
- **Claude Code (Sonnet 5.5):** wrote the skeleton, demo app, backend, and workflow. Wrote tests first and verified the planted bug live. Read logs to diagnose the workflow failures. It checked the Gemini action's inputs against its docs instead of guessing.
- **Gemini CLI (`gemini-3.5-flash-lite`):** the fix agent. The default model returned 503 "high demand" and used up half the free daily quota on retries; the Flash Lite model succeeded on the first try. The fix was correct, but the PR also included log files that I had to ignore.
- **Where it fell short:** the first workflow versions failed (workspace trust, model overload), and the action's output folder got committed. Things I could not verify without running them: the Sentry payload format.
