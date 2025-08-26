import asyncio
import logging
from asyncio import Task
from typing import Final, cast

from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq import Context, TaskiqDepends
from taskiq.brokers.shared_broker import shared_task

from compressor.application.common.ports.sender import FileForSendInfoDTO, Sender
from compressor.application.common.views.files import CompressedFileView
from compressor.application.services.files.compressor import FileCompressorService
from compressor.application.services.files.contracts import CompressTextFileDTO
from compressor.domain.files.values.file_id import FileID
from compressor.infrastructure.task_manager.files.contracts import FileInfoDTO

logger: Final[logging.Logger] = logging.getLogger(__name__)


@shared_task(
    retry_on_error=True,
    max_retries=3,
    delay=15
)
@inject(patch_module=True)
async def compress_and_send_file_task(
        data: FileInfoDTO,
        service: FromDishka[FileCompressorService],
        sender: FromDishka[Sender],
        context: Context = TaskiqDepends()
) -> None:
    logger.info(
        "Running task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    dto: CompressTextFileDTO = CompressTextFileDTO(
        compressor_type=data.compressor_type,
        file_id=data.file_id
    )

    view: CompressedFileView = await service.compress(dto=dto)

    logger.info("Got file view: %s", view)

    logger.info("Sending compressed file to user: %s", data.user_id)

    tasks: set[Task] = set()

    task: Task = asyncio.create_task(sender.send_file(
        user_id=data.user_id,
        file=FileForSendInfoDTO(
            file_id=cast("FileID", view.file_id)
        )
    ))
    tasks.add(task)

    task.add_done_callback(tasks.discard)

    logger.info("Successfully sent compressed file to user: %s", data.user_id)
