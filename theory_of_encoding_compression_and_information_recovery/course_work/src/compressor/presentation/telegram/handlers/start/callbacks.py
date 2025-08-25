from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from compressor.application.commands.user.signup import (
    SignUpCommand,
    SignUpCommandHandler
)
from compressor.domain.users.errors import SmallPasswordLength


@inject
async def register_handler_callback(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        interactor: FromDishka[SignUpCommandHandler]
) -> None:
    command: SignUpCommand = SignUpCommand(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        password=manager.dialog_data["password"],
    )


    try:
        await interactor(data=command)
    except SmallPasswordLength as e:
        await message.reply("Слишком слабый пароль! Введите получше!")
        await manager.back()
    else:
        await message.delete()
        await manager.next()
