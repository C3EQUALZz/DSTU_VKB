from abc import ABC

from app.application.jobs.factory import JobFactory
from app.infrastructure.services.image import ImageService
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.types.handlers import (
    CT,
    ET,
)


class ImagesEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow


class ImagesCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: UsersUnitOfWork, image_service: ImageService, job_factory: JobFactory) -> None:
        self._uow: UsersUnitOfWork = uow
        self._image_service: ImageService = image_service
        self._factory: JobFactory = job_factory
