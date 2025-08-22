from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from compressor.application.commands.register_via_telegram import (
    RegisterViaTelegramCommandHandler,
    RegisterViaTelegramCommand
)

@inject
async def register_handler_callback(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        interactor: FromDishka[RegisterViaTelegramCommandHandler]
) -> None:
    command: RegisterViaTelegramCommand = RegisterViaTelegramCommand(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        password=message_input.get_widget_data(DialogManager, default=""),
    )
    await interactor(data=command)
    await manager.next()
