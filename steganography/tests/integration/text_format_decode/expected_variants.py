"""Эталонные результаты декодирования реальных variantXX.docx.

Зафиксированы по прогону детектора на файлах, предоставленных
преподавателем. variant03 в источнике содержит наложение сокрытия и
декоративного форматирования стиха и в осмысленный текст не
декодируется — помечен как known-failure.
"""

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)

# filename -> (param, encoding_name, expected_message)
EXPECTED: dict[str, tuple[FormattingParam, str, str]] = {
    "variant01.docx": (
        FormattingParam.COLOR, "КОИ-8R", "Завтра подует завтрашний ветер.",
    ),
    "variant02.docx": (
        FormattingParam.SPACING, "Windows-1251",
        "Пусть не хвалят, лишь бы не ругали.",
    ),
    "variant04.docx": (
        FormattingParam.SPACING, "cp866",
        "В споре побеждает тот, кто громче кричит.",
    ),
    "variant05.docx": (
        FormattingParam.SCALE, "Windows-1251", "У других цветы красней.",
    ),
    "variant06.docx": (
        FormattingParam.COLOR, "cp866", "Все, что цветет, неизбежно увянет.",
    ),
    "variant07.docx": (
        FormattingParam.SCALE, "cp866",
        "Где права сила, там бессильно право.",
    ),
    "variant08.docx": (
        FormattingParam.COLOR, "Windows-1251",
        "Прямой человек, что прямой бамбук, встречается редко.",
    ),
    "variant09.docx": (
        FormattingParam.SIZE, "КОИ-8R",
        "Женщина захочет ) сквозь скалу пройдет.",
    ),
    "variant10.docx": (
        FormattingParam.SIZE, "cp866",
        "Баклажан на стебле дыни не вырастет.",
    ),
    "variant11.docx": (
        FormattingParam.SCALE, "КОИ-8R", "И мотылек живет целую жизнь.",
    ),
    "variant12.docx": (
        FormattingParam.SIZE, "Windows-1251",
        "Пятьдесят сегодня лучше, чем сто завтра.",
    ),
    "variant13.docx": (
        FormattingParam.SIZE, "КОИ-8R", "Крупная рыба в болоте не водится.",
    ),
    "variant14.docx": (
        FormattingParam.COLOR, "КОИ-8R", "Нет врага опаснее дурака.",
    ),
    "variant15.docx": (
        FormattingParam.SIZE, "cp866", "Ветер дует, но горы не двигаются.",
    ),
    "variant16.docx": (
        FormattingParam.SPACING, "КОИ-8R", "Об обычаях не спорят.",
    ),
    "variant17.docx": (
        FormattingParam.SIZE, "Windows-1251",
        "Один бог забыл ) другой поможет.",
    ),
    "variant18.docx": (
        FormattingParam.SPACING, "cp866", "Дела говорят громче слов.",
    ),
    "variant19.docx": (
        FormattingParam.SCALE, "Windows-1251", "Пустая бочка громче гремит.",
    ),
    "variant20.docx": (
        FormattingParam.COLOR, "cp866",
        "Бесполезнее, чем писать цифры на текущей воде.",
    ),
    "variant21.docx": (
        FormattingParam.SPACING, "КОИ-8R", "Конец болтовни ) начало дела.",
    ),
    "variant22.docx": (
        FormattingParam.COLOR, "Windows-1251", "Таланты не наследуют.",
    ),
    "variant23.docx": (
        FormattingParam.SCALE, "КОИ-8R",
        "Никто не спотыкается, лежа в постели.",
    ),
    "variant24.docx": (
        FormattingParam.SPACING, "Windows-1251",
        "Уступай дорогу дуракам и сумасшедшим.",
    ),
    "variant25.docx": (
        FormattingParam.COLOR, "Windows-1251",
        "Ячмень у соседа вкуснее риса дома.",
    ),
}

KNOWN_FAILURES: frozenset[str] = frozenset({"variant03.docx"})
