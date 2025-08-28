from typing import TYPE_CHECKING, cast

from typing_extensions import override

from compressor.infrastructure.task_manager.files.base import FileTaskManager
from compressor.infrastructure.task_manager.files.contracts import FileInfoDTO
from compressor.infrastructure.task_manager.files.tasks import compress_and_send_file_task, decompress_and_send_file
from compressor.infrastructure.task_manager.task_id import TaskID

if TYPE_CHECKING:
    from taskiq import AsyncTaskiqTask


class TaskIQFileTaskManager(FileTaskManager):
    @override
    async def compress_and_send_file(self, dto: FileInfoDTO) -> TaskID:
        task: AsyncTaskiqTask = await compress_and_send_file_task.kiq(data=dto)
        return cast("TaskID", task.task_id)

    @override
    async def decompress_and_send_file(self, dto: FileInfoDTO) -> TaskID:
        task: AsyncTaskiqTask = await decompress_and_send_file.kiq(data=dto)
        return cast("TaskID", task.task_id)
