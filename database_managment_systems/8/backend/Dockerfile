FROM python:3.12.1-slim-bullseye AS builder

COPY poetry.lock pyproject.toml ./

RUN python -m pip install poetry==1.8.4 && \
    poetry export -o requirements.prod.txt --without-hashes

FROM python:3.12.1-slim-bullseye AS dev

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

COPY --from=builder requirements.prod.txt /app

RUN apt update -y && \
    apt install -y python3-dev && \
    pip install --upgrade pip && pip install --no-cache-dir -r requirements.prod.txt

COPY . /app/