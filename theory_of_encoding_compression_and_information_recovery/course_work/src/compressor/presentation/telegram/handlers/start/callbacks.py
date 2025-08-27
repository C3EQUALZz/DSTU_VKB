from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities.modes import ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from compressor.application.commands.user.link_telegram_account import (
    LinkTelegramAccountCommand,
    LinkTelegramAccountCommandHandler,
)
from compressor.application.commands.user.signup import SignUpCommand, SignUpCommandHandler
from compressor.domain.users.errors import SmallPasswordLength
from compressor.presentation.errors.telegram import MessageCantBeNoneError, UserCantBeNoneError

if TYPE_CHECKING:
    from compressor.application.common.views.users import SignUpView


@inject
async def register_handler_callback(
    message: Message,
    message_input: MessageInput,  # noqa: ARG001
    manager: DialogManager,
    interactor: FromDishka[SignUpCommandHandler],
) -> None:
    user: User | None = message.from_user
    msg: str | None

    if user is None:
        msg = "User entity must be provided"
        raise UserCantBeNoneError(msg)

    if message.text is None:
        msg = "Message cant be None, text must be provided"
        raise MessageCantBeNoneError(msg)

    sign_in_command: SignUpCommand = SignUpCommand(
        username=user.username if user.username else user.first_name,
        password=message.text,
    )

    try:
        view: SignUpView = await interactor(data=sign_in_command)
        manager.dialog_data["sign_up_view_user_id"] = str(view.user_id)
    except SmallPasswordLength:
        await message.reply("Слишком слабый пароль! Введите получше!")
        await manager.back()
    else:
        await message.delete()
        await manager.next(show_mode=ShowMode.EDIT)


@inject
async def link_telegram_to_user_callback(
    callback: CallbackQuery,
    button: Button,  # noqa: ARG001
    manager: DialogManager,
    interactor: FromDishka[LinkTelegramAccountCommandHandler],
) -> None:
    user: User | None = callback.from_user
    user_id: str | None = manager.dialog_data["sign_up_view_user_id"]
    msg: str

    if user is None:
        msg = "User entity must be provided"
        raise UserCantBeNoneError(msg)

    if user_id is None:
        msg = "no provided info about user"
        raise UserCantBeNoneError(msg)

    link_command: LinkTelegramAccountCommand = LinkTelegramAccountCommand(
        user_id=UUID(user_id),
        telegram_id=user.id,
        first_name=user.first_name,
        username=user.username,
        last_name=user.last_name,
        is_premium=user.is_premium,
        is_bot=user.is_bot,
    )

    await interactor(link_command)
    await manager.next(show_mode=ShowMode.EDIT)
