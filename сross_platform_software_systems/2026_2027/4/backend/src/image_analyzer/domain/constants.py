from typing import Final

KNOWN_FOLDER_LABELS: Final[dict[str, str]] = {
    "0": "circle",
    "3": "triangle",
    "4": "square",
}


def label_for_folder(folder_name: str) -> str:
    return KNOWN_FOLDER_LABELS.get(folder_name, folder_name)
