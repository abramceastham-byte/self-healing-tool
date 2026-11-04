import hashlib
import hmac
import json
import os

from fastapi import FastAPI, HTTPException, Request, Response

app = FastAPI(title="Self-Heal Backend")


def signature_is_valid(body: bytes, signature: str | None) -> bool:
    secret = os.environ.get("SENTRY_WEBHOOK_SECRET")
    if not secret or not signature:
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def extract_issue(payload: dict) -> dict | None:
    data = payload.get("data") or {}
    event = data.get("event") or {}
    issue = data.get("issue") or {}
    issue_id = event.get("issue_id") or issue.get("id")
    if not issue_id:
        return None
    return {
        "issue_id": str(issue_id),
        "title": event.get("title") or issue.get("title") or "",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/webhooks/sentry")
async def sentry_webhook(request: Request, response: Response):
    body = await request.body()
    if not signature_is_valid(body, request.headers.get("Sentry-Hook-Signature")):
        raise HTTPException(status_code=401, detail="Invalid signature")
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    issue = extract_issue(payload)
    if issue is None:
        return {"accepted": False, "reason": "no issue in payload"}
    response.status_code = 202
    return {"accepted": True, **issue}
