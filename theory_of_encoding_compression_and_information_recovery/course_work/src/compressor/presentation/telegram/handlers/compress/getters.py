from typing import Any, Final

from aiogram_dialog import DialogManager

from compressor.presentation.errors.telegram import TaskIdNotProviderError

SUPPORTED_BINARY_OR_TEXT_FILE_COMPRESSORS: Final[tuple[tuple[str, str], ...]] = (
    ("xz", "1"),
    ("pigz", "2"),
    ("gzip", "3"),
    ("fastlz", "4"),
    ("bzip2", "5"),
)


async def get_compression_for_binary_or_text_files(**kwargs: Any) -> dict[str, Any]:  # noqa: ANN401, ARG001
    return {
        "compressor_algorithms": SUPPORTED_BINARY_OR_TEXT_FILE_COMPRESSORS,
        "count": len(SUPPORTED_BINARY_OR_TEXT_FILE_COMPRESSORS),
    }


async def task_id_getter(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401, ARG001
    task_id: str | None = dialog_manager.dialog_data.get("task_id")
    msg: str

    if task_id is None:
        msg = "task id not provided"
        raise TaskIdNotProviderError(msg)

    return {
        "task_id": task_id,
    }
