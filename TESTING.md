# Testing guide (Project 3.3)

Thanks for testing! This is a **prototype**. Here's what works today and how to try it in about 15 minutes.

**Spoiler warning:** `docs/planted-bugs.md` is the answer key for the demo app's bug. Please try to find the bug yourself before you read it.

## What it does
The full tool watches a GitHub repo for production errors, has an AI agent write a failing test and a fix, and opens a pull request with a plain-language summary.

**Works in this release**
- `demo-app/`: a small product-reviews web app with one planted bug.
- `backend/`: receives Sentry webhooks and checks their signature.
- The **Self-heal** GitHub Action in the demo app repo: you give it an error, an AI agent (Gemini) writes a test and a fix, a guard script blocks edits to protected files, the tests run, and a PR is opened.

**Not built yet:** Sentry is not wired to the Action (you type the error in by hand), and there's no deploy, rollback, notifications, database, or dashboard.

## Requirements
- Git and Python 3.11+ (3.12 recommended)
- Optional: [uv](https://docs.astral.sh/uv/) (faster installs)
- For part 3 only: a GitHub account and a free Gemini API key from https://aistudio.google.com/apikey

## 1. Install and run the demo app
```bash
git clone --recurse-submodules https://github.com/abramceastham-byte/self-healing-tool.git
cd self-healing-tool/demo-app
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```
**Ubuntu/WSL:** if `python3 -m venv` says "ensurepip is not available", either run `sudo apt install python3-venv` or use uv instead:
```bash
uv venv .venv && uv pip install -p .venv -r requirements-dev.txt
.venv/bin/uvicorn app.main:app --reload
```

Open http://localhost:8000 and click around. One product is broken. Can you find which one, and what happens?

Also try the API docs at http://localhost:8000/docs (add a product, add reviews, get ratings).

## 2. Run the tests
```bash
# in demo-app/ (venv active)
pytest

# backend
cd ../backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```
Expected: 13 tests pass in `demo-app`, 6 in `backend`. The existing tests do **not** catch the planted bug. That's on purpose.

## 3. Watch the AI fix the bug (optional, ~10 min)
This part runs in your own fork, so you use your own free Gemini key.

1. Fork https://github.com/abramceastham-byte/selfheal-demo-app
2. In your fork, open the **Actions** tab and click the button that enables workflows (forks start with them turned off).
3. Go to **Settings → Actions → General → Workflow permissions**. Select **Read and write permissions**, check **Allow GitHub Actions to create and approve pull requests**, and click Save.
4. Go to **Settings → Secrets and variables → Actions → New repository secret**. Name it `GEMINI_API_KEY` and paste your key as the value.
5. Go to **Actions → Self-heal → Run workflow** and fill in:
   - **error_id:** `test-1`
   - **error_title:** the error you saw in part 1 (for example the exception name and message from the uvicorn terminal)
   - **stack_trace:** paste the traceback from the uvicorn terminal
6. Wait about 2–4 minutes. If it succeeds, there's a new PR in your fork. Read the summary and the "Files changed" tab.

If you skip this part, you can look at the PRs the agent already opened: https://github.com/abramceastham-byte/selfheal-demo-app/pulls?q=is%3Apr

## Feedback I'm looking for
Please post in the class thread, or open a GitHub Issue on this repo for each problem (that makes it easy for me to track fixes).

1. **Setup:** Where did you get stuck? Was any step unclear or wrong for your OS?
2. **Bug hunt:** Did you find the broken product? Was the error obvious?
3. **AI fix:** If you ran part 3, did it work? Was the PR summary clear to a non-expert? Was the fix and test reasonable?
4. **Usefulness:** Would you connect this to your own project? What would stop you?
5. **Trust and safety:** What would you need to see before letting it auto-deploy a fix?
6. Anything else: bugs, confusing names, missing docs.
