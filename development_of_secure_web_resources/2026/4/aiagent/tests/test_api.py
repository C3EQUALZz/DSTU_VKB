import pytest
from fastapi.testclient import TestClient

import llm
from courses import COURSES, SHOP_TERMS
from main import app


@pytest.fixture
def client(monkeypatch):
    async def fake_answer(messages):
        return "Основы Python: 4900 ₽"

    monkeypatch.setattr(llm, "get_chat_answer", fake_answer)
    with TestClient(app) as test_client:
        yield test_client


def test_catalog_page_and_terms(client):
    assert client.get("/api/courses").json() == COURSES
    assert len(COURSES) == 3
    assert [course["price"] for course in COURSES] == [4900, 7900, 5900]
    assert client.get("/api/terms").json() == SHOP_TERMS
    assert client.get("/").status_code == 200
    assert 'lang="ru"' in client.get("/").text
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/static/styles.css").status_code == 200
    assert client.get("/docs").status_code == 200
    assert client.get("/.local.env").status_code == 404


def test_chat_trims_and_passes_history(client, monkeypatch):
    received = []

    async def answer(messages):
        received.extend(messages)
        return "4 недели"

    monkeypatch.setattr(llm, "get_chat_answer", answer)
    history = [
        {"role": "user", "content": " Python "},
        {"role": "assistant", "content": "4900 ₽"},
        {"role": "user", "content": "А сколько он длится?"},
    ]
    response = client.post("/api/chat", json={"messages": history})
    assert response.status_code == 200
    assert response.json() == {"answer": "4 недели"}
    assert received == [{**history[0], "content": "Python"}, *history[1:]]


@pytest.mark.parametrize("payload", [
    {}, {"messages": []},
    {"messages": [{"role": "user", "content": "x"}] * 21},
    {"messages": [{"role": "user", "content": " "}]},
    {"messages": [{"role": "user", "content": "x" * 2001}]},
    {"messages": [{"role": "system", "content": "x"}]},
    {"messages": [{"role": "assistant", "content": "x"}]},
    {"messages": [{"role": "user", "content": "x", "key": "x"}]},
    {"messages": [{"role": "user", "content": "x"}], "model": "x"},
    {"messages": [{"role": "user", "content": 123}]},
])
def test_invalid_input(client, payload):
    assert client.post("/api/chat", json=payload).status_code == 422


def test_maximum_valid_input(client):
    payload = {"messages": [{"role": "user", "content": "x" * 2000}] * 20}
    assert client.post("/api/chat", json=payload).status_code == 200


@pytest.mark.parametrize("code", [429, 502, 503, 504])
def test_safe_errors_and_independent_catalog(client, monkeypatch, code):
    async def fail(messages):
        raise llm.ChatError(code, "Безопасное сообщение")

    monkeypatch.setattr(llm, "get_chat_answer", fail)
    response = client.post("/api/chat", json={"messages": [{"role": "user", "content": "Привет"}]})
    assert response.status_code == code
    assert response.json() == {"detail": "Безопасное сообщение"}
    assert client.get("/api/courses").status_code == 200
