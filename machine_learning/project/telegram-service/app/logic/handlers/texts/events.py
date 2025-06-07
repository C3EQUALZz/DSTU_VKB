from app.infrastructure.scheduler.tasks.texts.schemas import TextForSendToChatSchema
from app.logic.events.texts import TextFromBrokerEvent
from app.logic.handlers.texts.base import TextsEventHandler
from app.settings.configs.enums import TaskNamesConfig


class TextFromBrokerEventHandler(TextsEventHandler[TextFromBrokerEvent]):
    async def __call__(self, event: TextFromBrokerEvent) -> None:
        await self._scheduler.schedule_task(
            TaskNamesConfig.SEND_TEXT_TO_USER,
            schemas=TextForSendToChatSchema(
                chat_id=event.chat_id,
                content=event.content,
            )
        )
