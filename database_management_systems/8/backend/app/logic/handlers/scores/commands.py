from typing import List

from app.domain.entities.score import ScoreEntity
from app.exceptions.infrastructure import (
    ScoreNotFoundException,
    UserNotFoundException,
)
from app.infrastructure.services.scores import ScoreService
from app.logic.commands.scores import (
    CreateScoreCommand,
    DeleteScoreCommand,
    GetAllScoresCommand,
    GetAllUserScoresCommand,
    GetScoreByIdCommand,
    UpdateScoreCommand,
)
from app.logic.handlers.scores.base import ScoreCommandHandler


class CreateScoreCommandHandler(ScoreCommandHandler[CreateScoreCommand]):
    async def __call__(self, command: CreateScoreCommand) -> ScoreEntity:
        score_service: ScoreService = ScoreService(uow=self._uow)
        new_score: ScoreEntity = ScoreEntity(**await command.to_dict())
        return await score_service.add(new_score)


class GetAllScoresCommandHandler(ScoreCommandHandler[GetAllScoresCommand]):
    async def __call__(self, command: GetAllScoresCommand) -> List[ScoreEntity]:
        score_service: ScoreService = ScoreService(uow=self._uow)
        return await score_service.get_all(**await command.to_dict())


class GetScoreByIdCommandHandler(ScoreCommandHandler[GetScoreByIdCommand]):
    async def __call__(self, command: GetScoreByIdCommand) -> ScoreEntity:
        score_service: ScoreService = ScoreService(uow=self._uow)
        return await score_service.get_by_id(oid=command.oid)


class UpdateScoreCommandHandler(ScoreCommandHandler[UpdateScoreCommand]):
    async def __call__(self, command: UpdateScoreCommand) -> ScoreEntity:
        score_service: ScoreService = ScoreService(uow=self._uow)

        if not score_service.check_existence(oid=command.score_oid):
            raise ScoreNotFoundException(command.score_oid)

        score: ScoreEntity = await score_service.get_by_id(command.score_oid)

        updated_score = ScoreEntity(**await command.to_dict())
        updated_score.oid = score.oid

        return await score_service.update(**await command.to_dict())


class DeleteScoreCommandHandler(ScoreCommandHandler[DeleteScoreCommand]):
    async def __call__(self, command: DeleteScoreCommand) -> None:
        score_service: ScoreService = ScoreService(uow=self._uow)

        if not score_service.check_existence(oid=command.score_oid):
            raise ScoreNotFoundException(str(command.score_oid))

        return await score_service.delete(oid=command.score_oid)


class GetAllUserScoresCommandHandler(ScoreCommandHandler[GetAllUserScoresCommand]):
    async def __call__(self, command: GetAllUserScoresCommand) -> List[ScoreEntity]:
        score_service: ScoreService = ScoreService(uow=self._uow)

        if not score_service.check_existence(user_oid=command.user_oid):
            raise UserNotFoundException(str(command.user_oid))

        scores: List[ScoreEntity] = await score_service.get_by_user_oid(user_oid=command.user_oid)

        return scores
