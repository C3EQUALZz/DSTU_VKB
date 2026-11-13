# AG2 и FastMCP: проверенные роли и короткий пример

Проверено 13 ноября 2026 года. Использованы официальные репозитории и документация. Установка, сетевой запуск сервера и LLM-вызовы не выполнялись. Версии библиотек в проекте пользователя неизвестны.

## Роли в презентации

| Technology | Role | Suitable slide wording |
|---|---|---|
| RAG | Архитектурный подход: поиск внешних данных перед/во время генерации | “RAG supplies relevant evidence to the model.” |
| GraphRAG | Использование графовых представлений для организации/поиска информации | “GraphRAG connects entities and supports broader questions.” |
| Agentic RAG | Выбор этапов поиска моделью, возможные повторные запросы | “An agent decides when to retrieve more evidence.” |
| AG2 | Framework для агентов, инструментов и их взаимодействия | “AG2 coordinates agents and tool use.” |
| FastMCP | Python framework для MCP servers/clients | “FastMCP exposes Python functions as MCP tools.” |

AG2 и FastMCP — библиотеки для реализации системы. Их присутствие само по себе не означает, что система реализует RAG, GraphRAG, проверку фактов или экономию денег.

## AG2: важное различие актуального и Classic API

[Официальный AG2 README](https://github.com/ag2ai/ag2/blob/main/README.md) прямо различает:

- **AG2 v1:** `import ag2`, основная сущность `Agent`.
- **AG2 Classic:** `import autogen`, `ConversableAgent`, `AssistantAgent`, `GroupChat`; отдельный [репозиторий](https://github.com/ag2ai/ag2-classic) и [документация](https://classic.docs.ag2.ai/).

Поэтому фраза “AG2 uses `from autogen import ConversableAgent`” допустима с уточнением **AG2 Classic**, если это соответствует реальному проекту пользователя. Нельзя без подтверждения версии считать этот импорт актуальным универсальным API AG2. На слайде безопаснее указать только **AG2 — agent orchestration**; версия и класс не обязательны для объяснения архитектуры.

[Classic Quickstart](https://classic.docs.ag2.ai/latest/docs/home/quickstart/) показывает `ConversableAgent`, `LLMConfig`, `.run(..., max_turns=3)` и конфигурацию провайдера. Этот пример требует provider dependency и API credentials, поэтому короткий слайдовый пример с придуманной моделью не нужен.

### Интеграция с MCP

[Текущая документация AG2 MCP Servers](https://docs.ag2.ai/docs/user-guide/tools/mcp_servers/) описывает `MCPToolkit`: framework подключается к существующему MCP server и предоставляет его инструменты агенту. Документирован как HTTP, так и локальный stdio transport. Это возможная интеграция; она не подтверждает способ подключения в проекте пользователя.

Шесть строк актуального **конфигурационного** примера; не самодостаточное приложение:

```python
from ag2 import Agent
from ag2.tools import MCPToolkit
agent = Agent(
    name="Security assistant",
    tools=[MCPToolkit("http://localhost:8000/mcp")],
)
```

Для выполнения нужен соответствующий HTTP server на указанном адресе и выбранная конфигурация модели. Этот пример относится к AG2 v1; для реального кейса с Classic его нельзя представлять как исходный код пользователя. Рекомендация: AG2 оставить в схеме, а реальный минимальный code snippet дать через FastMCP ниже.

## FastMCP: официальный проект и API

Старая ссылка [jlowin/fastmcp](https://github.com/jlowin/fastmcp) сейчас перенаправляет на [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp). Официальный сайт — [gofastmcp.com](https://gofastmcp.com/).

[Quickstart](https://gofastmcp.com/docs/getting-started/quickstart) подтверждает `from fastmcp import FastMCP`, `FastMCP("name")`, tool decorator и `mcp.run()`. По умолчанию используется local stdio; HTTP transport выбирается явно. Клиент — `from fastmcp import Client`, async context manager и `.call_tool(...)`.

[Tools](https://gofastmcp.com/docs/servers/tools) подтверждает параметры `description`, типизацию входов/выходов и превращение Python function в MCP tool с входной схемой. Пакет `fastmcp` и встроенный в MCP SDK вариант `mcp.server.fastmcp` — разные пути импорта; не смешивать их на одном примере.

### Рабочий учебный server — 8 строк

```python
from fastmcp import FastMCP
mcp = FastMCP("Security guidance")
GUIDANCE = {"secret_scan": "Review findings; never print secrets."}
@mcp.tool(description="Look up curated security guidance.")
def lookup_guidance(topic: str) -> str:
    return GUIDANCE.get(topic, "No matching guidance.")
if __name__ == "__main__":
    mcp.run()
```

Подпись на слайде: **Minimal FastMCP tool example**. Dictionary и текст правила написаны для учебного примера; это не пользовательская production database. Файл содержит полный минимальный server entrypoint, который можно запустить как `python guidance_server.py` в среде с установленным `fastmcp`. Здесь выполнена только синтаксическая проверка; успешный запуск с конкретной версией пакета не проверялся.

Пример выполняет точный lookup по одному ключу и возвращает строку. Семантический поиск, граф, reranking, модель, agent orchestration и citations добавляются другими компонентами. Не подписывать это как complete RAG или GraphRAG implementation. Статическая демонстрация не требует API key и не выполняет shell commands/сканирование/изменение CI.

## Применение к схеме CI: только то, что можно утверждать

Подходящая иллюстративная схема:

```text
CI event / finding
        ↓
Agent orchestration (AG2)
        ↓
MCP tool connection
        ↓
Guidance / retrieval tools (FastMCP)
        ↓
Relevant evidence → model response → human review
```

Эта схема — возможное разделение ответственности, а не восстановленная архитектура пользовательского проекта. GraphRAG может быть частью retrieval backend, Agentic RAG — логикой выбора дальнейших действий. Без дополнительных данных не обозначать конкретные vector DB, model provider, graph storage, pipeline platform, число агентов, измеренные расходы или результаты.

Для реального CI-кейса можно объяснить архитектурное ограничение: инструмент предоставляет только нужные операции; решение о допуске операции должно обеспечиваться приложением. Декоратор и текст инструкции не создают систему прав доступа. [FastMCP authorization](https://gofastmcp.com/docs/servers/authorization) различает проверку личности и проверку разрешений. Минимальный локальный example выше демонстрирует только curated lookup и не претендует на сетевое развёртывание с аутентификацией.

## Что использовать в 12 слайдах

- **AG2** и **FastMCP** — подписи двух частей архитектуры личного кейса.
- **8-line FastMCP example** — один читаемый code block рядом с объяснением полезности tools.
- **GraphRAG** и **Agentic RAG** — подходы к работе с evidence, отдельные от библиотек.
- Официальные источники — в notes/DOCX; версии user stack и performance не придумывать.
