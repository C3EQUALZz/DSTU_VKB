from io import BytesIO
from typing import Any

from aiogram import Bot
from aiogram.types import CallbackQuery, Document, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from compressor.application.commands.files.compress import CompressFileCommand, CompressFileCommandHandler
from compressor.application.common.views.tasks import TaskView
from compressor.presentation.errors.telegram import AlgorithmNotProvidedError, DocumentNotProvidedError
from compressor.presentation.telegram.handlers.compress.getters import SUPPORTED_BINARY_OR_TEXT_FILE_COMPRESSORS


async def start_compress_binary_or_text_file_subdialog(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager
) -> None:
    await manager.start(

    )


async def on_algorithm_selected(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: str
) -> None:
    manager.dialog_data["selected_algorithm_id"] = item_id
    await manager.next()


@inject
async def compress_binary_or_text_file(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        interactor: FromDishka[CompressFileCommandHandler]
) -> None:
    bot: Bot = manager.middleware_data["bot"]
    algorithm_id: str | None = manager.dialog_data.get("selected_algorithm_id", None)
    document: Document | None = message.document

    if algorithm_id is None:
        raise AlgorithmNotProvidedError("Algorithm must be provided")

    if document is None:
        raise DocumentNotProvidedError("Document must be provided")

    algorithm: str = next(filter(
        lambda pair_with_name_and_id: pair_with_name_and_id[1] == algorithm_id,
        SUPPORTED_BINARY_OR_TEXT_FILE_COMPRESSORS
    ), "gzip")

    data: BytesIO = BytesIO()

    await bot.download(document.file_id, destination=data)

    file_name: str = document.file_name if document.file_name is None else document.file_id

    command: CompressFileCommand = CompressFileCommand(
        compressor_type=algorithm,
        file_name=file_name,
        data=data
    )

    view: TaskView = await interactor(command)

    manager.dialog_data["task_id"] = view.task_id

    await manager.next()
