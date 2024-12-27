from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateScore(AbstractCommand):
    user_oid: str
    value: int


@dataclass(frozen=True)
class GetScoreById(AbstractCommand):
    oid: str
