# Микросервис изображений

Здесь микросервис, который отвечает за обработку изображений, где используются различные зависимости, начиная от `OpenCV`, заканчивая `Tenserflow`. 

На момент заполнения документации есть следующий функционал: 

- [`Перевод цветного изображения в серый`](app/infrastructure/integrations/color_to_gray)
- [`Ухудшение качества изображения`](app/infrastructure/integrations/compress)
- [`Обрезка изображения`](app/infrastructure/integrations/crop)
- [`Перевод из серого в цветное`](app/infrastructure/integrations/gray_to_color)
- [`Инверсия цветового пространства изображения`](app/infrastructure/integrations/inversion)
- [`Поворот изображения`](app/infrastructure/integrations/rotation)
- [`Стилизация первого изображения по стилю второго`](app/infrastructure/integrations/stylization)
