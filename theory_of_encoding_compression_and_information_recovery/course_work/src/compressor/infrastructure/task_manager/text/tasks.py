import logging
from typing import Final

from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq import Context, TaskiqDepends
from taskiq.brokers.shared_broker import shared_task

from compressor.application.commands.compression.text.compression import (
    CompressTextFileCommandHandler,
    CompressTextFileCommand
)
from compressor.application.common.ports.sender import Sender, FileForSendInfoDTO
from compressor.application.common.views.files import CompressedFileView
from compressor.infrastructure.task_manager.text.contracts import FileInfoDTO

logger: Final[logging.Logger] = logging.getLogger(__name__)


@shared_task(
    retry_on_error=True,
    max_retries=3,
    delay=15
)
@inject(patch_module=True)
async def compress_and_send_file_task(
        data: FileInfoDTO,
        interactor: FromDishka[CompressTextFileCommandHandler],
        sender: FromDishka[Sender],
        context: Context = TaskiqDepends()
) -> None:
    logger.info(
        "Running task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    command: CompressTextFileCommand = CompressTextFileCommand(
        compressor_type=str(data.compressor_type),
        path=data.file_path
    )

    compressed_file_view: CompressedFileView = await interactor(command)
    logger.info("Got file view: %s", compressed_file_view)

    logger.info("Sending compressed file to user: %s", data.user_id)

    await sender.send_file(
        user_id=data.user_id,
        file=FileForSendInfoDTO(path=compressed_file_view.path)
    )

    logger.info("Successfully sent compressed file to user: %s", data.user_id)

