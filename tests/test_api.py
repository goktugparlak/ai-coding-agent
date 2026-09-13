from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["llm_connected"] is False


def test_chat_help():
    response = client.post(
        "/api/chat",
        json={"message": "help"},
    )

    assert response.status_code == 200
    assert "Available commands" in response.json()["response"]
