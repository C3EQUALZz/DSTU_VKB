from abc import ABC

from app.infrastructure.scheduler.base import BaseScheduler
from app.infrastructure.services.transform import ImageTransformService
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.types.handlers import (
    CT,
    ET,
)


class ImageTransformEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(
            self,
            event_buffer: EventBuffer,
            scheduler: BaseScheduler
    ) -> None:
        self._event_buffer: EventBuffer = event_buffer
        self._scheduler: BaseScheduler = scheduler


class ImageTransformCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(
            self,
            event_buffer: EventBuffer,
            image_transform_service: ImageTransformService,
    ) -> None:
        self._event_buffer: EventBuffer = event_buffer
        self._image_transform_service: ImageTransformService = image_transform_service
