from aiogram.types import Message, User
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from compressor.application.commands.user.signup import SignUpCommand, SignUpCommandHandler
from compressor.domain.users.errors import SmallPasswordLength
from compressor.presentation.errors.telegram import MessageCantBeNoneError, UserCantBeNoneError


@inject
async def register_handler_callback(
    message: Message, message_input: MessageInput, manager: DialogManager, interactor: FromDishka[SignUpCommandHandler]
) -> None:
    user: User | None = message.from_user
    msg: str | None

    if user is None:
        msg = "User entity must be provided"
        raise UserCantBeNoneError(msg)

    if message.text is None:
        msg = "Message cant be None, text must be provided"
        raise MessageCantBeNoneError(msg)

    command: SignUpCommand = SignUpCommand(
        username=user.username if user.username else user.first_name,
        password=message.text,
    )

    try:
        await interactor(data=command)
    except SmallPasswordLength:
        await message.reply("Слишком слабый пароль! Введите получше!")
        await manager.back()
    else:
        await message.delete()
        await manager.next()
