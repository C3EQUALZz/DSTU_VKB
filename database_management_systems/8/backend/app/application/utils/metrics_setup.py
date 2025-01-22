from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


async def setup_metrics(app: FastAPI) -> None:
    instrumental = Instrumentator(
        excluded_handlers=["/metrics"],
        should_group_status_codes=False
    )
    instrumental.instrument(app).expose(app, tags=["metrics"], include_in_schema=False)
