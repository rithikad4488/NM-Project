from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_validation():
    response = client.post("/generate", json={
        "document_type": "",
        "parties": "A",
        "terms": "B",
        "effective_date": "2026-10-07",
    })
    assert response.status_code == 422
