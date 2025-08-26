from typing import cast

from taskiq import AsyncTaskiqTask
from typing_extensions import override

from compressor.infrastructure.task_manager.files.base import FileTaskManager
from compressor.infrastructure.task_manager.files.contracts import FileInfoDTO
from compressor.infrastructure.task_manager.files.tasks import compress_and_send_file_task
from compressor.infrastructure.task_manager.task_id import TaskID


class TaskIQFileTaskManager(FileTaskManager):
    @override
    async def compress_and_send_file(self, dto: FileInfoDTO) -> TaskID:
        task: AsyncTaskiqTask = await compress_and_send_file_task.kiq(dto=dto)
        return cast("TaskID", task.task_id)

    @override
    async def decompress_and_send_file(self, dto: FileInfoDTO) -> TaskID:
        ...
