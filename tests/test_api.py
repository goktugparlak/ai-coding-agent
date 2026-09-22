import pytest
from fastapi.testclient import TestClient

from app import api
from app.agent import CodingAgent
from app.database import HistoryStore
from app.providers.mock_provider import MockProvider


@pytest.fixture
def client(tmp_path):

    api.agent = CodingAgent(
        provider=MockProvider(),
        history=HistoryStore(
            tmp_path / "api-history.db"
        ),
    )

    return TestClient(api.app)


def test_health(client):

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["provider"] == "mock"
    assert data["llm_connected"] is False


def test_chat_help(client):

    response = client.post(
        "/api/chat",
        json={
            "message": "help"
        },
    )

    assert response.status_code == 200

    assert (
        "Available commands"
        in response.json()["response"]
    )