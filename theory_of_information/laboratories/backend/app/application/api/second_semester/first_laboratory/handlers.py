import logging

from fastapi import APIRouter, HTTPException
from app.application.api.second_semester.first_laboratory.schemas import MathExpressionRequestSchema
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.exceptions.base import ApplicationException
from app.logic.commands.field_calculator import EvaluateExpressionInField
from app.logic.use_cases.calculator import EvaluateMathExpressionInFieldUseCase

router = APIRouter(
    prefix="/second_semester/first_laboratory",
    tags=["second_semester", "first_laboratory"],
    route_class=DishkaRoute
)

logger = logging.getLogger(__name__)


@router.post(
    "/calculate",
    status_code=200,
    summary="This handler for evaluate expression in math field",
    description="Ex1: 9+2*3/7-8 (mod 11)"
)
async def calculate(
        schema: MathExpressionRequestSchema,
        use_case: FromDishka[EvaluateMathExpressionInFieldUseCase],
) -> int:
    try:
        command: EvaluateExpressionInField = EvaluateExpressionInField(**schema.model_dump())
        return await use_case(command)
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e.message))
