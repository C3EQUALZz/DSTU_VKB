from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException
from starlette import status

from app.application.api.scores.schemas import CreateScoreSchemeRequest, ScoreSchemeResponse, GetAllScoreSchemeRequest
from app.core.types.handlers import EventHandlerMapping, CommandHandlerMapping
from app.exceptions import ApplicationException
from app.infrastructure.uow.scores.base import ScoresUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.scores import CreateScoreCommand
from app.logic.message_bus import MessageBus

router = APIRouter(
    prefix="/scores",
    tags=["scores"],
    route_class=DishkaRoute,
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={

    },
    summary="Creates or adds a new score for the player",
)
async def create_score(
        scheme: CreateScoreSchemeRequest,
        uow: FromDishka[ScoresUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping]
) -> ScoreSchemeResponse:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=uow,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands
        )

        messagebus: MessageBus = await bootstrap.get_messagebus()

        await messagebus.handle(CreateScoreCommand(**scheme.model_dump()))

        return ScoreSchemeResponse.from_entity(messagebus.command_result)

    except ApplicationException as e:
        raise HTTPException(status_code=e.status, detail=str(e))


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={},
    summary="Gets all scores for each player",
)
async def get_all_scores(
        scheme: GetAllScoreSchemeRequest,
        uow: FromDishka[ScoresUnitOfWork],
        events: FromDishka[EventHandlerMapping],
        commands: FromDishka[CommandHandlerMapping]
) -> List[ScoreSchemeResponse]:
    ...


@router.get(
    "/{score_id}/",
    status_code=status.HTTP_200_OK,
    responses={},
    summary="Gets a score by his id",
)
async def get_score_by_id(score_id: str):
    ...


@router.patch(
    "/{score_id}/",
    status_code=status.HTTP_200_OK,
    responses={},
    summary="Updates a score by his id",
)
async def update_score(score_id: str):
    ...


@router.delete(
    "/{score_id}/",
    status_code=status.HTTP_200_OK,
    responses={},
    summary="Deletes a score by his id",
)
async def delete_score(score_id: str):
    ...


@router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    responses={},
    summary="Gets a user's score by his id",
)
async def get_user_score(user_id: str):
    ...
