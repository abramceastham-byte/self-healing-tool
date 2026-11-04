# Self-Healing Tool

Plugs into a GitHub repo, catches production errors with Sentry, has an AI agent write a failing test and a fix, opens a PR with a plain-language summary, deploys it, rolls back if errors increase, and notifies you on Discord, Slack, or email.

Stack: FastAPI on Railway, Neon PostgreSQL, React on Vercel, Claude Code or Codex in GitHub Actions. All free tiers.

## Status
- [x] Project skeleton and `CLAUDE.md`
- [x] `demo-app/` with a planted bug (see `demo-app/README.md`)
- [x] Backend: Sentry webhook endpoint with signature check
- [x] Agent workflow (Gemini) in the demo app repo: writes a test and a fix, opens a PR
- [ ] Sentry-to-workflow trigger, deploy, rollback, notifications, Neon, dashboard

`demo-app/` is a git submodule (its own repo, so the workflow runs in it). Clone with `git clone --recurse-submodules`.

See `CLAUDE.md` for architecture, layout, and how to run each part.

## AI Use
This project documents AI tool use as required by the class.
- **Claude Code** (Anthropic) generated the project skeleton, `CLAUDE.md`, the demo app (`demo-app/`) with its tests and the planted bug documentation in `docs/planted-bugs.md`, the backend webhook endpoint with its tests, and the self-heal GitHub workflow.
- **Gemini** (Google, via Gemini CLI in GitHub Actions, model `gemini-3.5-flash-lite`) is the fix agent in the prototype. It wrote the fix and test in the demo app's first automated PR.
- The finished tool uses AI agents (Claude Code or Codex in GitHub Actions) to write tests and fixes for production errors. Those PRs will be labeled as AI-generated.
- All AI output is reviewed by me before use.
