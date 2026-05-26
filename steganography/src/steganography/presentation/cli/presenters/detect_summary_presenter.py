"""DetectSummaryPresenter — сводная таблица по нескольким контейнерам."""

from typing import Final, final

from prettytable import PrettyTable

from steganography.application.common.views.text_format_decode import (
    DetectSecretView,
)


@final
class DetectSummaryPresenter:
    """Формирует PrettyTable-сводку по результатам пакетного анализа."""

    _MAX_MESSAGE_PREVIEW: Final[int] = 60
    _ELLIPSIS: Final[str] = "..."

    def render(self, views: list[DetectSecretView]) -> PrettyTable:
        table: PrettyTable = PrettyTable()
        table.title = "Сводка анализа контейнеров"
        table.field_names = ["Файл", "Параметр", "Кодировка", "Сообщение"]
        for col in ("Файл", "Параметр", "Кодировка", "Сообщение"):
            table.align[col] = "l"
        for v in views:
            table.add_row(self._row_for(v))
        return table

    def _row_for(self, view: DetectSecretView) -> list[str]:
        if not view.success or view.method is None or view.encoding is None:
            return [view.docx_path.name, "—", "—", f"ошибка: {view.error}"]
        return [
            view.docx_path.name,
            view.method.param.human_name,
            view.encoding.name,
            self._preview(view.message),
        ]

    def _preview(self, message: str) -> str:
        text: str = message.strip()
        if len(text) <= self._MAX_MESSAGE_PREVIEW:
            return text
        cutoff: int = self._MAX_MESSAGE_PREVIEW - len(self._ELLIPSIS)
        return text[:cutoff] + self._ELLIPSIS
