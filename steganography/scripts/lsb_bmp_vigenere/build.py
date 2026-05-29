"""Сборка docx-отчёта по ПР6 «LSB в BMP с шифрованием Виженера»."""

import asyncio
import sys
from pathlib import Path

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

from steganography.application.commands.lsb_bmp_vigenere.embed import (  # noqa: E402
    EmbedLsbBmpCommand,
    EmbedLsbBmpCommandHandler,
)
from steganography.application.commands.lsb_bmp_vigenere.extract import (  # noqa: E402
    ExtractLsbBmpCommand,
    ExtractLsbBmpCommandHandler,
)
from steganography.domain.lsb_bmp_vigenere.services.lsb_embedder import (  # noqa: E402
    LsbEmbedder,
)
from steganography.domain.lsb_bmp_vigenere.services.lsb_extractor import (  # noqa: E402
    LsbExtractor,
)
from steganography.domain.lsb_bmp_vigenere.services.marker_packager import (  # noqa: E402
    MarkerPackager,
)
from steganography.domain.lsb_bmp_vigenere.services.secret_embedder import (  # noqa: E402
    SecretEmbedder,
)
from steganography.domain.lsb_bmp_vigenere.services.secret_extractor import (  # noqa: E402
    SecretExtractor,
)
from steganography.domain.lsb_bmp_vigenere.services.vigenere_cipher import (  # noqa: E402
    VigenereCipher,
)
from steganography.infrastructure.bmp.pillow_bmp_reader import PillowBmpReader  # noqa: E402
from steganography.infrastructure.bmp.pillow_bmp_writer import PillowBmpWriter  # noqa: E402

_SAMPLE = _ROOT / "resources" / "bmp_samples" / "sample_64.bmp"
_OUTPUT_BMP = _ROOT / "resources" / "bmp_samples" / "stego_pr6.bmp"
_OUTPUT_DOCX = _ROOT / "docs" / "reports" / "2025" / "6" / "ПР6.docx"

_DEMO_SECRET = "Стеганография защищает данные от перехвата."
_DEMO_KEY = "MyKey-2025"


_META = LabMeta(
    number=6,
    title="LSB-стеганография в BMP с шифрованием Виженера",
    work_kind="Практическая работа",
    variant=None,
)

_GOAL = (
    "Познакомиться с методом замены наименее значащего бита (LSB) для "
    "сокрытия информации в неподвижных изображениях. Реализовать "
    "программу встраивания текстового сообщения в 24-битный BMP-"
    "контейнер с предварительным криптографическим кодированием "
    "(модифицированный шифр Виженера) и обёрткой полезной нагрузки "
    "управляющими метками начала/конца."
)

_THEORY = (
    "В методе LSB младший бит каждого канала пикселя (R, G, B) "
    "несёт один бит секретного сообщения. Поскольку для 8-битного "
    "канала изменение младшего бита визуально незаметно, контейнер "
    "сохраняет внешний вид при ёмкости до 3 бит на пиксель. Для защиты "
    "содержимого сообщение предварительно шифруется потоковым шифром "
    "Виженера mod 256, а для надёжного выделения полезной нагрузки в "
    "потоке LSB-битов используются метки начала и конца."
)

_TASK_ITEMS = (
    "реализовать чтение BMP-файла и доступ к каналам RGB его пикселей;",
    "реализовать модифицированный шифр Виженера (mod 256) для байтового потока;",
    "обернуть шифротекст метками начала и конца, как в методичке;",
    "встроить байты в младшие биты каналов изображения и сохранить новый BMP;",
    "реализовать обратную операцию извлечения и расшифровки сообщения.",
)

_ARCH_BULLETS = (
    "domain/common/bmp/ — общие VO Pixel/BmpImage и Protocol-порты BmpReader/BmpWriter (используются также в ПР7).",
    "domain/lsb_bmp_vigenere/services/vigenere_cipher.py — Виженер по байтам mod 256.",
    "domain/lsb_bmp_vigenere/services/marker_packager.py — обёртка start/end-марками.",
    "domain/lsb_bmp_vigenere/services/lsb_embedder.py / lsb_extractor.py — низкоуровневая вставка/извлечение LSB.",
    "domain/lsb_bmp_vigenere/services/secret_embedder.py / secret_extractor.py — высокоуровневые операции «зашифровать+встроить» / «извлечь+расшифровать».",
    "infrastructure/bmp/ — реализация BmpReader/BmpWriter через Pillow.",
    "application/commands/lsb_bmp_vigenere/{embed,extract}.py — async Command Handlers.",
    "presentation/cli/handlers/lsb_bmp_vigenere.py — click-команды с инжектом через dishka.",
)

_VIGENERE_LISTING = '''\
class VigenereCipher:
    """Симметричное шифрование байтового потока на основе ключа."""

    def encrypt(self, data: bytes, key: str) -> bytes:
        key_bytes = self._key_bytes(key)
        return bytes(
            (byte + key_bytes[index % len(key_bytes)]) % 256
            for index, byte in enumerate(data)
        )

    def decrypt(self, data: bytes, key: str) -> bytes:
        key_bytes = self._key_bytes(key)
        return bytes(
            (byte - key_bytes[index % len(key_bytes)]) % 256
            for index, byte in enumerate(data)
        )
'''

_LSB_LISTING = '''\
class LsbEmbedder:
    """Записывает байты сообщения в LSB каналов изображения."""

    def embed(self, image: BmpImage, payload: bytes) -> BmpImage:
        bits = self._bytes_to_bits(payload)
        capacity = image.total_pixels * 3
        if len(bits) > capacity:
            raise ContainerTooSmallError(
                required_bits=len(bits), available_bits=capacity,
            )

        flat_pixels = list(image.flatten())
        for bit_index, bit in enumerate(bits):
            pixel_index, channel_index = divmod(bit_index, 3)
            flat_pixels[pixel_index] = _set_channel_lsb(
                flat_pixels[pixel_index], channel_index, bit,
            )
        return BmpImage.from_flat(image.width, image.height, flat_pixels)
'''


def _embed_handler() -> EmbedLsbBmpCommandHandler:
    return EmbedLsbBmpCommandHandler(
        reader=PillowBmpReader(),
        writer=PillowBmpWriter(),
        embedder=SecretEmbedder(
            cipher=VigenereCipher(),
            packager=MarkerPackager(),
            embedder=LsbEmbedder(),
        ),
    )


def _extract_handler() -> ExtractLsbBmpCommandHandler:
    return ExtractLsbBmpCommandHandler(
        reader=PillowBmpReader(),
        extractor=SecretExtractor(
            cipher=VigenereCipher(),
            packager=MarkerPackager(),
            extractor=LsbExtractor(),
        ),
    )


async def _demo_run() -> tuple[int, int, str]:
    embed_view = await _embed_handler()(
        EmbedLsbBmpCommand(
            cover_path=_SAMPLE,
            output_path=_OUTPUT_BMP,
            secret_text=_DEMO_SECRET,
            key=_DEMO_KEY,
        ),
    )
    extract_view = await _extract_handler()(
        ExtractLsbBmpCommand(container_path=_OUTPUT_BMP, key=_DEMO_KEY),
    )
    return embed_view.payload_bits, embed_view.capacity_bits, extract_view.plaintext


def _build(payload_bits: int, capacity_bits: int, recovered: str) -> None:
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
        "Программа разделена на слои domain / application / infrastructure / "
        "presentation. BMP-инфраструктура вынесена в domain/common/bmp + "
        "infrastructure/bmp и переиспользуется ПР7.",
    )
    for bullet in _ARCH_BULLETS:
        add_para(doc, "• " + bullet, indent=False)

    add_heading(doc, "5. Ключевые фрагменты кода", level=2)
    add_label(doc, "Листинг 1 — модифицированный шифр Виженера")
    add_listing(doc, _VIGENERE_LISTING)
    add_label(doc, "Листинг 2 — встраивание байтов в LSB каналов")
    add_listing(doc, _LSB_LISTING)

    add_page_break(doc)
    add_heading(doc, "6. Демонстрация работы", level=2)
    add_para(
        doc,
        f"В качестве cover-контейнера использовано BMP-изображение "
        f"64×64 пикселя (resources/bmp_samples/sample_64.bmp). Полезная "
        f"нагрузка — сообщение «{_DEMO_SECRET}», ключ Виженера «{_DEMO_KEY}». "
        f"После встраивания и сохранения нового файла программа извлечения "
        f"восстановила сообщение целиком.",
    )
    ratio = payload_bits / capacity_bits if capacity_bits else 0.0
    add_table_simple(
        doc,
        rows=[
            ["Поле", "Значение"],
            ["Cover-контейнер", "resources/bmp_samples/sample_64.bmp"],
            ["Размер изображения", "64 × 64 пикселя"],
            ["Файл-результат", "resources/bmp_samples/stego_pr6.bmp"],
            ["Открытый текст", _DEMO_SECRET],
            ["Ключ", _DEMO_KEY],
            ["Полезных бит", str(payload_bits)],
            ["Ёмкость контейнера (бит)", str(capacity_bits)],
            ["Использовано ёмкости", f"{ratio:.2%}"],
            ["Восстановленное сообщение", recovered],
        ],
        caption="Таблица 1 — Параметры встраивания и результат извлечения",
    )

    add_heading(doc, "7. Вывод")
    add_para(
        doc,
        "В рамках практической работы реализован метод стеганографической "
        "защиты данных через встраивание шифротекста в младшие биты каналов "
        "BMP-изображения. Сообщение шифруется модифицированным Виженером "
        "(mod 256) и обрамляется метками; извлечение возможно только при "
        "наличии того же ключа. Поскольку изменение младших битов каналов "
        "визуально незаметно, контейнер сохраняет исходный вид. Полный "
        "цикл «зашифровать → встроить → извлечь → расшифровать» подтверждён "
        "программно: сообщение восстановлено без потерь.",
    )

    save(doc, _OUTPUT_DOCX)
    print(f"Отчёт сохранён: {_OUTPUT_DOCX}")


def main() -> None:
    payload_bits, capacity_bits, recovered = asyncio.run(_demo_run())
    _build(payload_bits, capacity_bits, recovered)


if __name__ == "__main__":
    main()
