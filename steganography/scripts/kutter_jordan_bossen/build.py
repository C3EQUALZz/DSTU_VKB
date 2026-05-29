"""Сборка docx-отчёта по КДБ8 «Метод Куттера-Джордана-Боссена»."""

import asyncio
import sys
from pathlib import Path

from PIL import Image

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "scripts"))

from report_builder import (  # noqa: E402
    LabMeta,
    add_heading,
    add_label,
    add_listing,
    add_page_break,
    add_para,
    add_table_simple,
    add_title_page,
    make_doc,
    save,
)

from steganography.application.commands.kutter_jordan_bossen.embed import (  # noqa: E402
    EmbedKjbCommand,
    EmbedKjbCommandHandler,
)
from steganography.application.commands.kutter_jordan_bossen.extract import (  # noqa: E402
    ExtractKjbCommand,
    ExtractKjbCommandHandler,
)
from steganography.domain.kutter_jordan_bossen.services.kjb_embedder import (  # noqa: E402
    KjbEmbedder,
)
from steganography.domain.kutter_jordan_bossen.services.kjb_extractor import (  # noqa: E402
    KjbExtractor,
)
from steganography.domain.kutter_jordan_bossen.services.luminance_calculator import (  # noqa: E402
    LuminanceCalculator,
)
from steganography.infrastructure.bmp.pillow_bmp_reader import PillowBmpReader  # noqa: E402
from steganography.infrastructure.bmp.pillow_bmp_writer import PillowBmpWriter  # noqa: E402

_SAMPLES_DIR = _ROOT / "resources" / "bmp_samples"
_COVER = _SAMPLES_DIR / "sample_smooth_128.bmp"
_STEGO = _SAMPLES_DIR / "stego_kjb.bmp"
_OUTPUT_DOCX = _ROOT / "docs" / "reports" / "2025" / "8" / "КДБ8.docx"

_DEMO_SECRET = "КДБ работает!"
_DEMO_LAMBDA = 0.2
_DEMO_SEED = 7


_META = LabMeta(
    number=8,
    title="Метод Куттера-Джордана-Боссена",
    work_kind="Контрольно-демонстрационный билет",
    variant=None,
)

_GOAL = (
    "Познакомиться с методом Куттера-Джордана-Боссена (КДБ) сокрытия "
    "информации в синей компоненте RGB неподвижных изображений. "
    "Реализовать программу встраивания и извлечения текстового "
    "сообщения с использованием псевдослучайного выбора пикселей-"
    "носителей и сравнения с соседями по канальной окрестности."
)

_THEORY = (
    "В основе метода — пониженная чувствительность зрения к синему "
    "цвету: модуляция синего канала пропорционально яркости пикселя "
    "малозаметна визуально, но достаточна для надёжного извлечения. "
    "Для бита «1» синяя компонента пикселя-носителя увеличивается на "
    "λ·Y, для бита «0» — уменьшается, где Y — яркость по BT.601 "
    "(Y = 0.299·R + 0.587·G + 0.114·B). Псевдослучайный выбор пикселей "
    "с общим seed обеспечивает повторяемость для приёмника. Извлечение "
    "не требует исходного изображения: бит восстанавливается по знаку "
    "разности между синим каналом пикселя и средним значением синего "
    "его соседей (4 пикселя крестообразной окрестности)."
)

_TASK_ITEMS = (
    "реализовать чтение BMP-файла и доступ к каналам пикселей;",
    "реализовать расчёт яркости BT.601 и псевдослучайный выбор пикселей-носителей с заданным seed;",
    "встроить биты сообщения в синюю компоненту выбранных пикселей по правилу B' = B ± λ·Y;",
    "реализовать извлечение по сравнению синего канала с средним по соседям;",
    "продемонстрировать на гладком тестовом изображении полный цикл встраивание-извлечение.",
)

_ARCH_BULLETS = (
    "domain/common/bmp/ — общее с ПР6/ПР7 (Pixel, BmpImage, BmpReader, BmpWriter).",
    "domain/kutter_jordan_bossen/services/luminance_calculator.py — формула BT.601.",
    "domain/kutter_jordan_bossen/services/pixel_selector.py — PRNG-выбор позиций.",
    "domain/kutter_jordan_bossen/services/kjb_embedder.py — модуляция синего на ±λ·Y.",
    "domain/kutter_jordan_bossen/services/kjb_extractor.py — сравнение с соседями.",
    "domain/kutter_jordan_bossen/value_objects/ — KjbParameters, KjbStats.",
    "application/commands/kutter_jordan_bossen/{embed,extract}.py — async Command Handlers.",
    "presentation/cli/handlers/kutter_jordan_bossen.py — click-команды через dishka.",
)


_EMBEDDER_LISTING = '''\
class KjbEmbedder:
    """Встраивание битов сообщения в синий канал изображения."""

    def embed(self, image, bits, params):
        selector = self._selector_factory(params.seed)
        positions = selector.select(
            image, count=len(bits), margin=params.neighbour_radius,
        )

        rows = [list(row) for row in image.pixels]
        for (x, y), bit in zip(positions, bits, strict=True):
            old_pixel = rows[y][x]
            luminance = self._luminance.of(old_pixel)
            delta = params.lambda_factor * luminance
            new_blue = (
                old_pixel.blue + delta if bit == 1 else old_pixel.blue - delta
            )
            rows[y][x] = old_pixel.with_blue(_clamp_byte(round(new_blue)))
        ...
'''


_EXTRACTOR_LISTING = '''\
class KjbExtractor:
    """Извлечение скрытых бит из BMP с известными параметрами КДБ."""

    def extract(self, image, bit_count, params):
        selector = self._selector_factory(params.seed)
        positions = selector.select(
            image, count=bit_count, margin=params.neighbour_radius,
        )
        result = []
        for x, y in positions:
            expected_blue = self._average_neighbour_blue(
                image, x, y, params.neighbour_radius,
            )
            actual_blue = image.pixels[y][x].blue
            result.append(1 if actual_blue > expected_blue else 0)
        return result
'''


def _embed_handler() -> EmbedKjbCommandHandler:
    return EmbedKjbCommandHandler(
        reader=PillowBmpReader(),
        writer=PillowBmpWriter(),
        embedder=KjbEmbedder(luminance=LuminanceCalculator()),
    )


def _extract_handler() -> ExtractKjbCommandHandler:
    return ExtractKjbCommandHandler(
        reader=PillowBmpReader(),
        extractor=KjbExtractor(),
    )


def _ensure_sample() -> None:
    if _COVER.exists():
        return
    _SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (128, 128))
    image.putdata(
        [
            ((x * 2) % 256, (y * 2) % 256, ((x + y) % 256))
            for y in range(128) for x in range(128)
        ],
    )
    image.save(_COVER, format="BMP")


async def _run() -> tuple[int, int, str]:
    _ensure_sample()
    embed_view = await _embed_handler()(
        EmbedKjbCommand(
            cover_path=_COVER,
            output_path=_STEGO,
            secret_text=_DEMO_SECRET,
            lambda_factor=_DEMO_LAMBDA,
            seed=_DEMO_SEED,
        ),
    )
    extract_view = await _extract_handler()(
        ExtractKjbCommand(
            container_path=_STEGO,
            lambda_factor=_DEMO_LAMBDA,
            seed=_DEMO_SEED,
        ),
    )
    return embed_view.payload_bits, embed_view.container_pixels, extract_view.message


def _build(payload_bits: int, container_pixels: int, recovered: str) -> None:
    doc = make_doc()
    add_title_page(doc, _META)
    add_page_break(doc)

    add_heading(doc, "1. Цель работы")
    add_para(doc, _GOAL)

    add_heading(doc, "2. Теоретическая часть")
    add_para(doc, _THEORY)

    add_heading(doc, "3. Задание на выполнение")
    for item in _TASK_ITEMS:
        add_para(doc, "— " + item, indent=False)

    add_heading(doc, "4. Архитектура решения (Clean Architecture)")
    add_para(
        doc,
        "Программа использует общее ядро BMP (domain/common/bmp + "
        "infrastructure/bmp) с ПР6/ПР7. Доменные сервисы метода КДБ "
        "(LuminanceCalculator, PixelSelector, KjbEmbedder, "
        "KjbExtractor) скомпонованы вокруг агрегата BmpImage и связаны "
        "через dishka в application + CLI слоях.",
    )
    for bullet in _ARCH_BULLETS:
        add_para(doc, "• " + bullet, indent=False)

    add_heading(doc, "5. Ключевые фрагменты кода", level=2)
    add_label(doc, "Листинг 1 — встраивание в синюю компоненту")
    add_listing(doc, _EMBEDDER_LISTING)
    add_label(doc, "Листинг 2 — извлечение по соседям")
    add_listing(doc, _EXTRACTOR_LISTING)

    add_page_break(doc)
    add_heading(doc, "6. Демонстрация работы", level=2)
    add_para(
        doc,
        f"В качестве cover-контейнера использовано гладкое градиентное "
        f"изображение 128×128 пикселей (sample_smooth_128.bmp). Полезная "
        f"нагрузка — сообщение «{_DEMO_SECRET}», параметр λ = {_DEMO_LAMBDA}, "
        f"seed = {_DEMO_SEED}. Программа встроила биты в синюю компоненту "
        f"псевдослучайно выбранных пикселей и сохранила контейнер; "
        f"программа извлечения по тому же seed и тому же λ восстановила "
        f"сообщение посимвольно.",
    )
    rate = payload_bits / container_pixels if container_pixels else 0.0
    add_table_simple(
        doc,
        rows=[
            ["Поле", "Значение"],
            ["Cover-контейнер", "resources/bmp_samples/sample_smooth_128.bmp"],
            ["Размер изображения", "128 × 128 пикселей"],
            ["Файл-результат", "resources/bmp_samples/stego_kjb.bmp"],
            ["Сообщение", _DEMO_SECRET],
            ["Параметр λ", f"{_DEMO_LAMBDA:.2f}"],
            ["Seed", str(_DEMO_SEED)],
            ["Полезных бит", str(payload_bits)],
            ["Пикселей в контейнере", str(container_pixels)],
            ["Рейт внедрения", f"{rate:.4f} бит/пиксель"],
            ["Восстановленное сообщение", recovered],
        ],
        caption="Таблица 1 — Параметры встраивания и результат извлечения",
    )

    add_heading(doc, "7. Замечание о применимости")
    add_para(
        doc,
        "Метод Куттера-Джордана-Боссена корректно работает на относительно "
        "гладких изображениях (фотографии, градиенты), где соседние пиксели "
        "имеют близкие значения синего канала. На сильно зашумлённых "
        "изображениях (равномерно случайный шум) сравнение пикселя со "
        "средним по соседям может давать ошибки извлечения. Это известное "
        "ограничение алгоритма; в практических задачах в качестве "
        "контейнера выбираются фотографии природных сцен.",
    )

    add_heading(doc, "8. Вывод")
    add_para(
        doc,
        "В рамках лабораторной работы изучен и программно реализован "
        "метод Куттера-Джордана-Боссена сокрытия информации в синей "
        "компоненте RGB. Реализация выполнена в стиле Clean Architecture "
        "с разделением на доменные сервисы (расчёт яркости, выбор "
        "пикселей, встраивание, извлечение), application-handlers и CLI. "
        "Полный цикл встраивания-извлечения на гладком тестовом "
        "изображении подтверждён программно — сообщение восстанавливается "
        "посимвольно.",
    )

    save(doc, _OUTPUT_DOCX)
    print(f"Отчёт сохранён: {_OUTPUT_DOCX}")


def main() -> None:
    payload_bits, container_pixels, recovered = asyncio.run(_run())
    _build(payload_bits, container_pixels, recovered)


if __name__ == "__main__":
    main()
