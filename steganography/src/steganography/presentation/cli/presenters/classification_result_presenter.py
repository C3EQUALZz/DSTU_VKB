"""ClassificationResultPresenter — табличный вывод результатов классификации."""

from typing import final

from prettytable import PrettyTable

from steganography.application.common.views.linguistic_bit_in_string import (
    ClassifyStringsView,
)


@final
class ClassificationResultPresenter:
    """Формирует PrettyTable с ответами «ДА/НЕТ» по каждой строке."""

    def render(self, view: ClassifyStringsView) -> PrettyTable:
        table: PrettyTable = PrettyTable()
        table.title = (
            f"Классификация {view.input_path.name} "
            f"(ДА: {view.yes_count}, НЕТ: {view.no_count})"
        )
        table.field_names = ["#", "Ответ", "Гласных", "Строка"]
        table.align["#"] = "r"
        table.align["Ответ"] = "l"
        table.align["Гласных"] = "r"
        table.align["Строка"] = "l"
        for index, item in enumerate(view.classifications, start=1):
            table.add_row(
                [
                    str(index),
                    item.answer,
                    str(item.feature_value),
                    item.text,
                ],
            )
        return table
