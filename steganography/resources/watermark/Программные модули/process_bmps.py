from PIL import Image, ImageFilter, ImageEnhance
import os
import numpy as np


def process_image(input_file, output_dir):
    """
    Применяет все виды обработки к BMP изображению
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = Image.open(input_file)
    filename = os.path.basename(input_file).replace('.bmp', '')

    print(f"\n=== Обработка файла: {input_file} ===")
    print(f"Исходный размер: {img.size}, режим: {img.mode}")
    original_size = os.path.getsize(input_file)
    print(f"Исходный размер файла: {original_size} байт")

    # ============================================
    # 1. АЛГОРИТМЫ АРХИВАЦИИ С ПОТЕРЯМИ
    # ============================================

    # Способ 1: Конвертация в JPEG и обратно в BMP
    img_rgb = img.convert('RGB')

    for quality in [90, 75, 50, 25]:
        temp_jpg = os.path.join(output_dir, f'{filename}_jpeg_q{quality}.jpg')
        output_bmp = os.path.join(output_dir, f'{filename}_jpeg_q{quality}_back.bmp')

        # Сохраняем как JPEG (с потерями)
        img_rgb.save(temp_jpg, 'JPEG', quality=quality, optimize=True)
        jpg_size = os.path.getsize(temp_jpg)

        # Загружаем обратно, конвертируем в 1-бит и сохраняем как BMP
        img_jpeg = Image.open(temp_jpg).convert('1')
        img_jpeg.save(output_bmp, 'BMP')
        bmp_size = os.path.getsize(output_bmp)

        os.remove(temp_jpg)

        print(f"  JPEG качество {quality}: JPEG={jpg_size} байт, BMP(1-бит)={bmp_size} байт")

    # Способ 2: Уменьшение цветовой глубины
    # 8-бит (256 оттенков серого)
    img_8bit = img.convert('L')  # Grayscale 8-bit
    output_8bit = os.path.join(output_dir, f'{filename}_8bit.bmp')
    img_8bit.save(output_8bit, 'BMP')
    print(f"  8-бит (grayscale): {os.path.getsize(output_8bit)} байт")

    # 4-бит (16 оттенков серого) - через палитру
    img_4bit = img.convert('L')
    # Уменьшаем количество уровней серого до 16
    img_4bit_array = np.array(img_4bit)
    img_4bit_array = (img_4bit_array // 16) * 16  # 16 уровней
    img_4bit = Image.fromarray(img_4bit_array)
    output_4bit = os.path.join(output_dir, f'{filename}_4bit.bmp')
    img_4bit.save(output_4bit, 'BMP')
    print(f"  4-бит (16 уровней): {os.path.getsize(output_4bit)} байт")

    # ============================================
    # 2. ПРЕОБРАЗОВАНИЯ ИЗОБРАЖЕНИЙ
    # ============================================

    # --- МОДИФИКАЦИЯ ---

    # Добавление шума
    img_gray = img.convert('L')
    img_array = np.array(img_gray)
    noise = np.random.randint(0, 50, img_array.shape, dtype=np.uint8)
    img_noisy = Image.fromarray(np.clip(img_array + noise, 0, 255).astype(np.uint8)).convert('1')
    output_noise = os.path.join(output_dir, f'{filename}_noise.bmp')
    img_noisy.save(output_noise, 'BMP')
    print(f"  С шумом: {os.path.getsize(output_noise)} байт")

    # Размытие
    img_blur = img.convert('RGB').filter(ImageFilter.GaussianBlur(radius=3)).convert('1')
    output_blur = os.path.join(output_dir, f'{filename}_blur.bmp')
    img_blur.save(output_blur, 'BMP')
    print(f"  Размытие: {os.path.getsize(output_blur)} байт")

    # Изменение яркости
    enhancer = ImageEnhance.Brightness(img.convert('RGB'))
    img_bright = enhancer.enhance(1.5).convert('1')
    output_bright = os.path.join(output_dir, f'{filename}_bright.bmp')
    img_bright.save(output_bright, 'BMP')
    print(f"  Яркость +50%: {os.path.getsize(output_bright)} байт")

    # Изменение контраста
    enhancer = ImageEnhance.Contrast(img.convert('RGB'))
    img_contrast = enhancer.enhance(1.5).convert('1')
    output_contrast = os.path.join(output_dir, f'{filename}_contrast.bmp')
    img_contrast.save(output_contrast, 'BMP')
    print(f"  Контраст +50%: {os.path.getsize(output_contrast)} байт")

    # Поворот
    img_rotated = img.convert('RGB').rotate(45, fillcolor=0).convert('1')
    output_rotated = os.path.join(output_dir, f'{filename}_rotated45.bmp')
    img_rotated.save(output_rotated, 'BMP')
    print(f"  Поворот 45°: {os.path.getsize(output_rotated)} байт")

    # --- ОБРЕЗАНИЕ КРАЕВ (CROP) ---

    width, height = img.size

    # Обрезать по 10% с каждой стороны
    crop_margin_x = int(width * 0.1)
    crop_margin_y = int(height * 0.1)
    img_cropped = img.crop((crop_margin_x, crop_margin_y,
                            width - crop_margin_x, height - crop_margin_y))
    output_cropped = os.path.join(output_dir, f'{filename}_cropped10.bmp')
    img_cropped.save(output_cropped, 'BMP')
    print(f"  Обрезка 10%: {img_cropped.size}, {os.path.getsize(output_cropped)} байт")

    # Обрезать по 20% с каждой стороны
    crop_margin_x = int(width * 0.2)
    crop_margin_y = int(height * 0.2)
    img_cropped2 = img.crop((crop_margin_x, crop_margin_y,
                             width - crop_margin_x, height - crop_margin_y))
    output_cropped2 = os.path.join(output_dir, f'{filename}_cropped20.bmp')
    img_cropped2.save(output_cropped2, 'BMP')
    print(f"  Обрезка 20%: {img_cropped2.size}, {os.path.getsize(output_cropped2)} байт")

    # Обрезать только снизу и справа
    img_cropped3 = img.crop((0, 0, int(width * 0.8), int(height * 0.8)))
    output_cropped3 = os.path.join(output_dir, f'{filename}_cropped_bottom_right.bmp')
    img_cropped3.save(output_cropped3, 'BMP')
    print(f"  Обрезка снизу-справа: {img_cropped3.size}, {os.path.getsize(output_cropped3)} байт")

    # --- МАСШТАБИРОВАНИЕ (RESIZE) ---

    # Уменьшить в 2 раза
    img_small = img.resize((width // 2, height // 2), Image.LANCZOS)
    output_small = os.path.join(output_dir, f'{filename}_scale_50.bmp')
    img_small.save(output_small, 'BMP')
    print(f"  Масштаб 50%: {img_small.size}, {os.path.getsize(output_small)} байт")

    # Уменьшить в 4 раза
    img_tiny = img.resize((width // 4, height // 4), Image.LANCZOS)
    output_tiny = os.path.join(output_dir, f'{filename}_scale_25.bmp')
    img_tiny.save(output_tiny, 'BMP')
    print(f"  Масштаб 25%: {img_tiny.size}, {os.path.getsize(output_tiny)} байт")

    # Увеличить в 1.5 раза
    img_large = img.resize((int(width * 1.5), int(height * 1.5)), Image.LANCZOS)
    output_large = os.path.join(output_dir, f'{filename}_scale_150.bmp')
    img_large.save(output_large, 'BMP')
    print(f"  Масштаб 150%: {img_large.size}, {os.path.getsize(output_large)} байт")

    print(f"\n✓ Все файлы сохранены в: {output_dir}")


# ============================================
# ЗАПУСК ОБРАБОТКИ
# ============================================

files_to_process = [
    '1_преим_белый-105-mod.bmp',
    '2_сбалансированный-105-mod.bmp',
    '3_преим_черный-105-mod.bmp'
]

for file in files_to_process:
    if os.path.exists(file):
        output_dir = f'processed_{file.replace(".bmp", "")}'
        process_image(file, output_dir)
    else:
        print(f"⚠ Файл не найден: {file}")

print("\n" + "=" * 50)
print("ОБРАБОТКА ЗАВЕРШЕНА!")
print("=" * 50)