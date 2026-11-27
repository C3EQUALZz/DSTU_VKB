import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from openai import APIConnectionError, APIStatusError, APITimeoutError

import llm
from courses import COURSES, SHOP_TERMS


@pytest.fixture(autouse=True)
def isolate_settings(monkeypatch, tmp_path):
    # Ни один тест не читает настоящий ключ и не обращается к сети.
    monkeypatch.setattr(llm, "ENV_FILE", tmp_path / ".local.env")
    for name in ("LLM_PROVIDER", "LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL", "YANDEX_FOLDER_ID"):
        monkeypatch.delenv(name, raising=False)


def configure(monkeypatch, provider="openai"):
    for name, value in {
        "LLM_PROVIDER": provider, "LLM_API_KEY": "test-only-placeholder",
        "LLM_BASE_URL": llm.PROVIDER_URLS[provider], "LLM_MODEL": "test-model",
    }.items():
        monkeypatch.setenv(name, value)
    if provider == "yandex":
        monkeypatch.setenv("YANDEX_FOLDER_ID", "test-folder")
        monkeypatch.setenv("LLM_MODEL", "gpt://test-folder/yandexgpt/latest")


def fake_client(monkeypatch, content="Ответ", choices=True):
    configure(monkeypatch)
    result = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))] if choices else [])
    create = AsyncMock(return_value=result)
    client = AsyncMock()
    client.chat.completions.create = create
    client.__aenter__.return_value = client
    client.__aexit__.return_value = False
    monkeypatch.setattr(llm, "AsyncOpenAI", MagicMock(return_value=client))
    return client, create


def test_context_and_history(monkeypatch):
    client, create = fake_client(monkeypatch, " Ответ ")
    history = [{"role": "user", "content": "Цена?"}]
    assert asyncio.run(llm.get_chat_answer(history)) == "Ответ"
    sent = create.call_args.kwargs
    assert sent["model"] == "test-model"
    assert sent["messages"][1:] == history
    system = sent["messages"][0]
    assert system["role"] == "system"
    for course in COURSES:
        assert course["title"] in system["content"]
        assert str(course["price"]) in system["content"]
        for topic in course["topics"]:
            assert topic in system["content"]
    for value in SHOP_TERMS["payment_methods"]:
        assert value in system["content"]
    assert "не придумывай" in system["content"].lower()


@pytest.mark.parametrize("provider", ["openai", "deepseek", "qwen", "yandex"])
def test_client_options_and_automatic_cleanup(monkeypatch, provider):
    fake, _ = fake_client(monkeypatch)
    configure(monkeypatch, provider)
    for _ in range(2):
        assert asyncio.run(llm.get_chat_answer([])) == "Ответ"
    assert llm.AsyncOpenAI.call_count == 2
    assert llm.AsyncOpenAI.call_args.kwargs == {"api_key": "test-only-placeholder", "base_url": llm.PROVIDER_URLS[provider], "project": "test-folder" if provider == "yandex" else None, "timeout": 30.0, "max_retries": 0}
    assert fake.__aenter__.await_count == 2
    assert fake.__aexit__.await_count == 2


def test_file_loading_and_environment_priority(monkeypatch):
    llm.ENV_FILE.write_text("LLM_PROVIDER=openai\nLLM_API_KEY=file-placeholder\nLLM_BASE_URL=https://api.openai.com/v1\nLLM_MODEL=file-model\n", encoding="utf-8")
    monkeypatch.setenv("LLM_MODEL", "environment-model")
    assert llm.load_settings() == ("file-placeholder", "https://api.openai.com/v1", "environment-model", None)


@pytest.mark.parametrize("name,value", [
    ("LLM_PROVIDER", "unknown"), ("LLM_API_KEY", ""), ("LLM_MODEL", ""),
    ("LLM_API_KEY", "YOUR_API_KEY"), ("LLM_MODEL", "YOUR_MODEL"),
    ("LLM_BASE_URL", "https://example.com"),
    ("LLM_BASE_URL", "https://api.deepseek.com"),
    ("LLM_BASE_URL", "http://api.openai.com/v1"),
])
def test_bad_settings_never_create_client(monkeypatch, name, value):
    configure(monkeypatch)
    monkeypatch.setenv(name, value)

    def forbidden(**kwargs):
        pytest.fail("При неверных настройках SDK не должен создаваться")

    monkeypatch.setattr(llm, "AsyncOpenAI", forbidden)
    with pytest.raises(llm.ChatError) as error:
        asyncio.run(llm.get_chat_answer([]))
    assert error.value.status_code == 503


def test_catalog_without_configuration():
    from fastapi.testclient import TestClient
    from main import app
    with TestClient(app) as client:
        assert client.get("/api/courses").status_code == 200
        response = client.post("/api/chat", json={"messages": [{"role": "user", "content": "Цена?"}]})
        assert response.status_code == 503
        assert "не настроен" in response.json()["detail"]


@pytest.mark.parametrize("http_status,code,expected", [
    (400, "invalid_request", 503), (401, "invalid_api_key", 503),
    (402, "insufficient_balance", 503), (403, "forbidden", 503), (404, "model_not_found", 503),
    (429, "insufficient_quota", 503), (429, "quota_exceeded", 503),
    (429, "rate_limit_exceeded", 429), (500, "server_error", 502),
])
def test_provider_errors(monkeypatch, http_status, code, expected):
    client, create = fake_client(monkeypatch)
    request = httpx.Request("POST", "https://example.com")
    response = httpx.Response(http_status, request=request)
    create.side_effect = APIStatusError("private provider details", response=response, body={"code": code})
    with pytest.raises(llm.ChatError) as error:
        asyncio.run(llm.get_chat_answer([]))
    assert error.value.status_code == expected
    assert "private" not in str(error.value)
    client.__aexit__.assert_awaited_once()


@pytest.mark.parametrize("timeout,expected", [(True, 504), (False, 502)])
def test_connection_errors(monkeypatch, timeout, expected):
    _, create = fake_client(monkeypatch)
    request = httpx.Request("POST", "https://example.com")
    create.side_effect = APITimeoutError(request=request) if timeout else APIConnectionError(request=request)
    with pytest.raises(llm.ChatError) as error:
        asyncio.run(llm.get_chat_answer([]))
    assert error.value.status_code == expected


@pytest.mark.parametrize("content,choices", [(None, True), ("   ", True), ("", True), ("", False)])
def test_empty_response(monkeypatch, content, choices):
    fake_client(monkeypatch, content, choices)
    with pytest.raises(llm.ChatError) as error:
        asyncio.run(llm.get_chat_answer([]))
    assert error.value.status_code == 502


@pytest.mark.parametrize("provider", ["openai", "yandex"])
@pytest.mark.parametrize("status_code", [200, 500])
def test_real_sdk_closes_http_client_without_network(monkeypatch, status_code, provider):
    from openai import AsyncOpenAI

    configure(monkeypatch, provider)
    requests = []

    def respond(request):
        requests.append(request)
        if status_code != 200:
            return httpx.Response(status_code, json={"error": {"message": "test failure"}})
        return httpx.Response(200, json={
            "id": "test", "object": "chat.completion", "created": 0, "model": "test-model",
            "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": "Ответ"}}],
        })

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(respond))
    monkeypatch.setattr(llm, "AsyncOpenAI", lambda **options: AsyncOpenAI(**options, http_client=http_client))
    if status_code == 200:
        assert asyncio.run(llm.get_chat_answer([{"role": "user", "content": "Цена?"}])) == "Ответ"
    else:
        with pytest.raises(llm.ChatError) as error:
            asyncio.run(llm.get_chat_answer([]))
        assert error.value.status_code == 502
    assert len(requests) == 1
    assert http_client.is_closed
    assert str(requests[0].url) == llm.PROVIDER_URLS[provider] + "/chat/completions"
    if provider == "yandex":
        import json
        assert requests[0].headers["OpenAI-Project"] == "test-folder"
        assert json.loads(requests[0].content)["model"] == "gpt://test-folder/yandexgpt/latest"


@pytest.mark.parametrize("folder,model", [
    ("", "gpt://test-folder/yandexgpt/latest"),
    ("YOUR_FOLDER_ID", "gpt://YOUR_FOLDER_ID/yandexgpt/latest"),
    ("test-folder", "gpt://other-folder/yandexgpt/latest"),
    ("test-folder", "yandexgpt/latest"),
    ("test-folder", "gpt://test-folder/"),
    ("test/folder", "gpt://test/folder/yandexgpt/latest"),
])
def test_yandex_bad_folder_or_model_never_calls_sdk(monkeypatch, folder, model):
    configure(monkeypatch, "yandex")
    monkeypatch.setenv("YANDEX_FOLDER_ID", folder)
    monkeypatch.setenv("LLM_MODEL", model)
    constructor = MagicMock()
    monkeypatch.setattr(llm, "AsyncOpenAI", constructor)
    with pytest.raises(llm.ChatError) as error:
        asyncio.run(llm.get_chat_answer([]))
    assert error.value.status_code == 503
    constructor.assert_not_called()


def test_yandex_file_and_folder_environment_priority(monkeypatch):
    llm.ENV_FILE.write_text(
        "LLM_PROVIDER=yandex\nLLM_API_KEY=test-placeholder\n"
        "LLM_BASE_URL=https://ai.api.cloud.yandex.net/v1/\n"
        "LLM_MODEL=gpt://file-folder/yandexgpt/latest\nYANDEX_FOLDER_ID=file-folder\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("YANDEX_FOLDER_ID", "environment-folder")
    monkeypatch.setenv("LLM_MODEL", "gpt://environment-folder/yandexgpt/latest")
    assert llm.load_settings() == (
        "test-placeholder", "https://ai.api.cloud.yandex.net/v1",
        "gpt://environment-folder/yandexgpt/latest", "environment-folder",
    )


def test_other_providers_ignore_yandex_folder(monkeypatch):
    configure(monkeypatch)
    monkeypatch.setenv("YANDEX_FOLDER_ID", "leftover-folder")
    assert llm.load_settings()[-1] is None


def test_yandex_missing_folder_does_not_break_catalog(monkeypatch):
    from fastapi.testclient import TestClient
    from main import app

    configure(monkeypatch, "yandex")
    monkeypatch.delenv("YANDEX_FOLDER_ID")
    with TestClient(app) as client:
        response = client.post("/api/chat", json={
            "messages": [{"role": "user", "content": "Цена?"}],
        })
        assert response.status_code == 503
        assert "YANDEX_FOLDER_ID" in response.json()["detail"]
        assert client.get("/api/courses").status_code == 200
