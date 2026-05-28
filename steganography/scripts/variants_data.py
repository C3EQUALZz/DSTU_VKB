"""Единая таблица 25 вариантов задания: пословица + метод + кодировка.

Используется генератором сгенерированных контейнеров (ПР2) и сборщиками
docx-отчётов по каждому из 25 вариантов (ПР1 и ПР2). Cover-индекс — это
номер стиха в ``resources/steganographic_concealment/covers/`` (от 1 до 10),
циклически назначенный варианту.
"""

from dataclasses import dataclass
from typing import Final

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)


@dataclass(frozen=True, slots=True)
class VariantSpec:
    number: int
    secret: str
    param: FormattingParam
    encoding_name: str

    @property
    def cover_index(self) -> int:
        return ((self.number - 1) % 10) + 1


VARIANTS: Final[tuple[VariantSpec, ...]] = (
    VariantSpec(1, "Завтра подует завтрашний ветер.",
                FormattingParam.COLOR, "КОИ-8R"),
    VariantSpec(2, "Пусть не хвалят, лишь бы не ругали.",
                FormattingParam.SPACING, "Windows-1251"),
    VariantSpec(3, "Терпение и труд всё перетрут.",
                FormattingParam.SIZE, "Windows-1251"),
    VariantSpec(4, "В споре побеждает тот, кто громче кричит.",
                FormattingParam.SPACING, "cp866"),
    VariantSpec(5, "У других цветы красней.",
                FormattingParam.SCALE, "Windows-1251"),
    VariantSpec(6, "Все, что цветет, неизбежно увянет.",
                FormattingParam.COLOR, "cp866"),
    VariantSpec(7, "Где права сила, там бессильно право.",
                FormattingParam.SCALE, "cp866"),
    VariantSpec(8, "Прямой человек, что прямой бамбук, встречается редко.",
                FormattingParam.COLOR, "Windows-1251"),
    VariantSpec(9, "Женщина захочет - сквозь скалу пройдет.",
                FormattingParam.SIZE, "КОИ-8R"),
    VariantSpec(10, "Баклажан на стебле дыни не вырастет.",
                FormattingParam.SIZE, "cp866"),
    VariantSpec(11, "И мотылек живет целую жизнь.",
                FormattingParam.SCALE, "КОИ-8R"),
    VariantSpec(12, "Пятьдесят сегодня лучше, чем сто завтра.",
                FormattingParam.SIZE, "Windows-1251"),
    VariantSpec(13, "Крупная рыба в болоте не водится.",
                FormattingParam.SIZE, "КОИ-8R"),
    VariantSpec(14, "Нет врага опаснее дурака.",
                FormattingParam.COLOR, "КОИ-8R"),
    VariantSpec(15, "Ветер дует, но горы не двигаются.",
                FormattingParam.SIZE, "cp866"),
    VariantSpec(16, "Об обычаях не спорят.",
                FormattingParam.SPACING, "КОИ-8R"),
    VariantSpec(17, "Один бог забыл - другой поможет.",
                FormattingParam.SIZE, "Windows-1251"),
    VariantSpec(18, "Дела говорят громче слов.",
                FormattingParam.SPACING, "cp866"),
    VariantSpec(19, "Пустая бочка громче гремит.",
                FormattingParam.SCALE, "Windows-1251"),
    VariantSpec(20, "Бесполезнее, чем писать цифры на текущей воде.",
                FormattingParam.COLOR, "cp866"),
    VariantSpec(21, "Конец болтовни - начало дела.",
                FormattingParam.SPACING, "КОИ-8R"),
    VariantSpec(22, "Таланты не наследуют.",
                FormattingParam.COLOR, "Windows-1251"),
    VariantSpec(23, "Никто не спотыкается, лежа в постели.",
                FormattingParam.SCALE, "КОИ-8R"),
    VariantSpec(24, "Уступай дорогу дуракам и сумасшедшим.",
                FormattingParam.SPACING, "Windows-1251"),
    VariantSpec(25, "Ячмень у соседа вкуснее риса дома.",
                FormattingParam.COLOR, "Windows-1251"),
)
