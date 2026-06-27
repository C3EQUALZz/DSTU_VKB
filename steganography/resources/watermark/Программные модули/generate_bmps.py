from PIL import Image, ImageDraw
import random
import math


def generate_monochrome_image(width, height, white_ratio, filename):
    """
    Генерирует монохромное BMP изображение с большими участками
    """
    # Создаем изображение
    if white_ratio > 0.5:
        # Белый доминирует - белый фон
        img = Image.new('1', (width, height), color=1)
        draw = ImageDraw.Draw(img)

        # Рисуем ЧЕРНЫЕ фигуры (меньшинство)
        num_black_shapes = int(20 * (1 - white_ratio))  # чем меньше белого, тем больше черных
        for _ in range(max(8, num_black_shapes)):
            size = random.randint(40, 120)
            x = random.randint(size // 2, width - size // 2)
            y = random.randint(size // 2, height - size // 2)

            shape_type = random.choice(['ellipse', 'rectangle', 'polygon'])
            if shape_type == 'ellipse':
                bbox = [x - size // 2, y - size // 2, x + size // 2, y + size // 2]
                draw.ellipse(bbox, fill=0)
            elif shape_type == 'rectangle':
                bbox = [x - size // 2, y - size // 2, x + size // 2, y + size // 2]
                draw.rectangle(bbox, fill=0)
            else:
                points = []
                num_points = random.randint(4, 8)
                for j in range(num_points):
                    angle = 2 * math.pi * j / num_points
                    r = size // 2 * random.uniform(0.5, 1.0)
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    points.append((px, py))
                draw.polygon(points, fill=0)

        # Добавляем черные линии
        num_lines = max(5, int(15 * (1 - white_ratio)))
        for _ in range(num_lines):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=0, width=random.randint(3, 8))

    elif white_ratio < 0.5:
        # Черный доминирует - черный фон
        img = Image.new('1', (width, height), color=0)
        draw = ImageDraw.Draw(img)

        # Рисуем БЕЛЫЕ фигуры (меньшинство)
        num_white_shapes = int(20 * white_ratio)  # чем меньше белого ratio, тем меньше белых фигур
        for _ in range(max(5, num_white_shapes)):
            size = random.randint(40, 120)
            x = random.randint(size // 2, width - size // 2)
            y = random.randint(size // 2, height - size // 2)

            shape_type = random.choice(['ellipse', 'rectangle', 'polygon'])
            if shape_type == 'ellipse':
                bbox = [x - size // 2, y - size // 2, x + size // 2, y + size // 2]
                draw.ellipse(bbox, fill=1)
            elif shape_type == 'rectangle':
                bbox = [x - size // 2, y - size // 2, x + size // 2, y + size // 2]
                draw.rectangle(bbox, fill=1)
            else:
                points = []
                num_points = random.randint(4, 8)
                for j in range(num_points):
                    angle = 2 * math.pi * j / num_points
                    r = size // 2 * random.uniform(0.5, 1.0)
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    points.append((px, py))
                draw.polygon(points, fill=1)

        # Добавляем белые линии
        num_lines = max(3, int(10 * white_ratio))
        for _ in range(num_lines):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=1, width=random.randint(3, 8))

    else:
        # Сбалансированный (50/50) - черный фон
        img = Image.new('1', (width, height), color=0)
        draw = ImageDraw.Draw(img)

        # Рисуем МНОГО белых фигур
        for _ in range(25):
            size = random.randint(40, 100)
            x = random.randint(size // 2, width - size // 2)
            y = random.randint(size // 2, height - size // 2)

            shape_type = random.choice(['ellipse', 'rectangle', 'polygon'])
            if shape_type == 'ellipse':
                bbox = [x - size // 2, y - size // 2, x + size // 2, y + size // 2]
                draw.ellipse(bbox, fill=1)
            elif shape_type == 'rectangle':
                bbox = [x - size // 2, y - size // 2, x + size // 2, y + size // 2]
                draw.rectangle(bbox, fill=1)
            else:
                points = []
                num_points = random.randint(4, 8)
                for j in range(num_points):
                    angle = 2 * math.pi * j / num_points
                    r = size // 2 * random.uniform(0.5, 1.0)
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    points.append((px, py))
                draw.polygon(points, fill=1)

        # Рисуем черные фигуры поверх (чтобы создать баланс)
        for _ in range(15):
            size = random.randint(30, 80)
            x = random.randint(size // 2, width - size // 2)
            y = random.randint(size // 2, height - size // 2)

            shape_type = random.choice(['ellipse', 'rectangle', 'polygon'])
            if shape_type == 'ellipse':
                bbox = [x - size // 2, y - size // 2, x + size // 2, y + size // 2]
                draw.ellipse(bbox, fill=0)
            elif shape_type == 'rectangle':
                bbox = [x - size // 2, y - size // 2, x + size // 2, y + size // 2]
                draw.rectangle(bbox, fill=0)
            else:
                points = []
                num_points = random.randint(4, 8)
                for j in range(num_points):
                    angle = 2 * math.pi * j / num_points
                    r = size // 2 * random.uniform(0.5, 1.0)
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    points.append((px, py))
                draw.polygon(points, fill=0)

        # Добавляем линии обоих цветов
        for _ in range(10):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=1, width=random.randint(3, 8))

        for _ in range(8):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=0, width=random.randint(3, 8))

    # Сохраняем как BMP
    img.save(filename, 'BMP')
    print(f"Создан файл: {filename} (белого: ~{white_ratio * 100:.0f}%)")


# Генерируем три изображения
width, height = 400, 400

# 1. Преимущественно белый (75% белого, 25% черного) - мало черных фигур
generate_monochrome_image(width, height, white_ratio=0.75, filename='1_преим_белый.bmp')

# 2. Сбалансированный (50% белого, 50% черного) - много фигур обоих цветов
generate_monochrome_image(width, height, white_ratio=0.50, filename='2_сбалансированный.bmp')

# 3. Преимущественно черный (25% белого, 75% черного) - мало белых фигур
generate_monochrome_image(width, height, white_ratio=0.25, filename='3_преим_черный.bmp')

print("\nВсе изображения созданы!")