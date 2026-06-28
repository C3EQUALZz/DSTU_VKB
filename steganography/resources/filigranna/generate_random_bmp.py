#!/usr/bin/env python3
"""Генератор случайного BMP-файла заданного размера (на основе Pillow).

Примеры:
    python generate_random_bmp.py 128 128
    python generate_random_bmp.py 256 256 -o noise.bmp
    python generate_random_bmp.py 64 64 --seed 42 --gray
"""

import argparse
import os
import random
from PIL import Image


def generate_bmp(width: int, height: int, out_path: str,
                 seed: int | None = None, gray: bool = False) -> None:
    """Создаёт случайный BMP размером width x height."""


    rng = random.Random(seed)
    if gray:
        img = Image.new("L", (width, height))
        img.putdata([rng.randint(0, 255) for _ in range(width * height)])
    else:
        img = Image.new("RGB", (width, height))
        img.putdata([(rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255))
                     for _ in range(width * height)])
    img.save(out_path, format="BMP")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Генерация случайного BMP заданного размера.")
    parser.add_argument("width", type=int, help="ширина в пикселях")
    parser.add_argument("height", type=int, help="высота в пикселях")
    parser.add_argument("-o", "--output", default=None,
                        help="имя выходного файла (по умолчанию random_<w>x<h>.bmp)")
    parser.add_argument("--seed", type=int, default=None,
                        help="зерно ГСЧ для воспроизводимости")
    parser.add_argument("--gray", action="store_true",
                        help="оттенки серого вместо цветного шума")
    args = parser.parse_args()

    if args.width <= 0 or args.height <= 0:
        parser.error("ширина и высота должны быть положительными")

    out_path = args.output or f"random_{args.width}x{args.height}.bmp"
    # Относительные пути — рядом со скриптом.
    if not os.path.isabs(out_path):
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), out_path)

    generate_bmp(args.width, args.height, out_path, args.seed, args.gray)
    print(f"Создан файл: {out_path} ({args.width}x{args.height}, "
          f"{os.path.getsize(out_path)} байт)")


if __name__ == "__main__":
    main()
