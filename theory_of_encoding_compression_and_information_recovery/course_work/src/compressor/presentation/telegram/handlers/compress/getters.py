from typing import Any, Final

from compressor.presentation.errors.telegram import TaskIdNotProviderError

SUPPORTED_BINARY_OR_TEXT_FILE_COMPRESSORS: Final[tuple[tuple[str, str], ...]] = (
    ("LZMA", "1"),
    ("PIGZ", "2"),
    ("GZIP", "3"),
    ("FASTLZ", "4"),
    ("BZIP2", "5"),
)


async def get_compression_for_binary_or_text_files(**kwargs) -> dict[str, Any]:
    return {
        "compressor_algorithms": SUPPORTED_BINARY_OR_TEXT_FILE_COMPRESSORS,
        "count": len(SUPPORTED_BINARY_OR_TEXT_FILE_COMPRESSORS),
    }

async def task_id_getter(dialog_data: dict[str, Any], **kwargs) -> dict[str, Any]:
    task_id: str | None = dialog_data.get("task_id")

    if task_id is None:
        raise TaskIdNotProviderError("task id not provided")

    return {
        "task_id": task_id,
    }
