import hashlib
import hmac
import json

import pytest
from fastapi.testclient import TestClient

from app.main import app

SECRET = "test-secret"


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("SENTRY_WEBHOOK_SECRET", SECRET)
    return TestClient(app)


def sign(body: bytes, secret=SECRET):
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def post(client, payload, signature=None, resource="event_alert"):
    body = json.dumps(payload).encode()
    headers = {
        "Content-Type": "application/json",
        "Sentry-Hook-Signature": signature if signature is not None else sign(body),
        "Sentry-Hook-Resource": resource,
    }
    return client.post("/webhooks/sentry", content=body, headers=headers)


ALERT = {
    "action": "triggered",
    "data": {
        "event": {
            "issue_id": "12345",
            "title": "ZeroDivisionError: division by zero",
            "web_url": "https://sentry.io/organizations/x/issues/12345/",
        }
    },
}


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_valid_alert_is_accepted(client):
    res = post(client, ALERT)
    assert res.status_code == 202
    assert res.json() == {
        "accepted": True,
        "issue_id": "12345",
        "title": "ZeroDivisionError: division by zero",
    }


def test_bad_signature_rejected(client):
    assert post(client, ALERT, signature="deadbeef").status_code == 401


def test_missing_signature_rejected(client):
    body = json.dumps(ALERT).encode()
    res = client.post("/webhooks/sentry", content=body)
    assert res.status_code == 401


def test_unconfigured_secret_rejects_everything(monkeypatch):
    monkeypatch.delenv("SENTRY_WEBHOOK_SECRET", raising=False)
    assert post(TestClient(app), ALERT).status_code == 401


def test_payload_without_issue_is_ignored(client):
    res = post(client, {"action": "triggered", "data": {}})
    assert res.status_code == 200
    assert res.json() == {"accepted": False, "reason": "no issue in payload"}
