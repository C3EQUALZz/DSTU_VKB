from typing import Final

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from app.infrastructure.metrics.base import BaseMetricsClient

router: Final[APIRouter] = APIRouter(
    prefix="",
    route_class=DishkaRoute,
    tags=["metrics"]
)


@router.get(
    "/metrics",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    summary="Handler for getting metrics from any provider",
    description="Return metrics from any provider",
    tags=["metrics"]
)
async def get_metrics(
        metrics_client: FromDishka[BaseMetricsClient]
) -> Response:
    """
    Return metrics
    """
    return Response(
        metrics_client.generate_latest(),
        media_type='text/plain; version=0.0.4; charset=utf-8'
    )
