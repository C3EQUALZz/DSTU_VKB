from app.domain.entities.message import TextMessageEntity
from app.infrastructure.uow.message.base import MessagesUnitOfWork


class MessageService:
    def __init__(self, uow: MessagesUnitOfWork) -> None:
        self._uow = uow

    async def send_text_message(self, message: TextMessageEntity) -> TextMessageEntity:
        """
        This method is used to send a text message for chat bot.
        :param message: entity message to be sent
        :return:
        """
        return await self._uow.text.send_message(message=message)