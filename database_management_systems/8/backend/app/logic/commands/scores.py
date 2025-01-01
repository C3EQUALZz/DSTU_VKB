from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateScoreCommand(AbstractCommand):
    user_oid: str
    value: int


@dataclass(frozen=True)
class GetAllScoresCommand(AbstractCommand):
    page_number: int
    page_size: int


@dataclass(frozen=True)
class GetScoreByIdCommand(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class UpdateScoreCommand(AbstractCommand):
    score_oid: str


@dataclass(frozen=True)
class DeleteScoreCommand(AbstractCommand):
    score_oid: str


@dataclass(frozen=True)
class GetAllUserScoresCommand(AbstractCommand):
    user_oid: str
    page_number: int
    page_size: int
