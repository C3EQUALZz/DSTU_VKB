"""FastAPI: проверяем входные данные и связываем страницу с моделью."""

from pathlib import Path
from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

import llm
from courses import COURSES, SHOP_TERMS

BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(title="Код / Курсы", description="Учебный магазин с ИИ-консультантом")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

MessageText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]


class Message(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["user", "assistant"]
    content: MessageText


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    messages: list[Message] = Field(
        min_length=1, max_length=20,
        examples=[[{"role": "user", "content": "Какой курс подойдет новичку?"}]],
    )

    @model_validator(mode="after")
    def last_message_is_user(self):
        if self.messages[-1].role != "user":
            raise ValueError("Последнее сообщение должно иметь роль user")
        return self


class ChatResponse(BaseModel):
    answer: str


class Course(BaseModel):
    id: str
    title: str
    description: str
    price: int = Field(gt=0)
    currency: Literal["RUB"]
    duration_weeks: int = Field(gt=0)
    duration_hours: int = Field(gt=0)
    topics: list[str]


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/courses", response_model=list[Course], summary="Три учебных курса")
async def courses():
    return COURSES


@app.get("/api/terms", summary="Условия учебного магазина")
async def terms():
    # И страница, и модель получают условия из одного места.
    return SHOP_TERMS


@app.post("/api/chat", response_model=ChatResponse, summary="Задать вопрос консультанту")
async def chat(request: ChatRequest):
    try:
        answer = await llm.get_chat_answer([message.model_dump() for message in request.messages])
    except llm.ChatError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from None
    return ChatResponse(answer=answer)
