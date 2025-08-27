from io import BytesIO
from typing import TYPE_CHECKING, Any

from aiogram.types import CallbackQuery, Document, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from compressor.application.commands.files.compress import CompressFileCommand, CompressFileCommandHandler
from compressor.presentation.errors.telegram import AlgorithmNotProvidedError, DocumentNotProvidedError
from compressor.presentation.telegram.handlers.compress.getters import SUPPORTED_BINARY_OR_TEXT_FILE_COMPRESSORS

if TYPE_CHECKING:
    from aiogram import Bot

    from compressor.application.common.views.tasks import TaskView


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
    msg: str

    if algorithm_id is None:
        msg = "Algorithm must be provided"
        raise AlgorithmNotProvidedError(msg)

    if document is None:
        msg = "Document must be provided"
        raise DocumentNotProvidedError(msg)

    algorithm: str = next(filter(
        lambda pair_with_name_and_id: pair_with_name_and_id[1] == algorithm_id,
        SUPPORTED_BINARY_OR_TEXT_FILE_COMPRESSORS
    ), "gzip")

    data: BytesIO = BytesIO()

    await bot.download(document.file_id, destination=data)

    file_name: str = document.file_name if document.file_name is not None else document.file_id

    command: CompressFileCommand = CompressFileCommand(
        compressor_type=algorithm,
        file_name=file_name,
        data=data
    )

    view: TaskView = await interactor(command)

    manager.dialog_data["task_id"] = view.task_id

    await manager.next()
