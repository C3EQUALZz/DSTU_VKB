from typing import Any

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from cryptography_methods.application.commands.atbash.decrypt import AtbashDecryptCommandHandler, AtbashDecryptCommand
from cryptography_methods.application.common.views.atbash import AtbashDecryptionView


async def decrypt_atbash_error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
) -> None:
    await message.answer("Должна быть введена обычная строка")


@inject
async def decrypt_atbash_handler(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        interactor: FromDishka[AtbashDecryptCommandHandler]
) -> None:
    text_from_message: str | None = message.text

    if text_from_message is None:
        raise ...

    command: AtbashDecryptCommand = AtbashDecryptCommand(
        text=text_from_message,
    )

    view: AtbashDecryptionView = await interactor(command)

    message_for_reply: str = (
        f"Ваше сообщение было зашифровано: '{view.decrypted_text}'"
    )
    await message.reply(text=message_for_reply)
    await manager.done(show_mode=ShowMode.NO_UPDATE)
