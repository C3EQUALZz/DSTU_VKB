# Микросервис изображений

Здесь микросервис, который отвечает за обработку изображений, где используются различные зависимости, начиная от `OpenCV`, заканчивая `Tenserflow`. 

На момент заполнения документации есть следующий функционал: 

- [`Перевод цветного изображения в серый`](machine_learning/project/image-service/app/infrastructure/integrations/color_to_gray)
- [`Ухудшение качества изображения`](machine_learning/project/image-service/app/infrastructure/integrations/compress)
- [`Обрезка изображения`](machine_learning/project/image-service/app/infrastructure/integrations/crop)
- [`Перевод из серого в цветное`](machine_learning/project/image-service/app/infrastructure/integrations/gray_to_color)
- [`Инверсия цветового пространства изображения`](machine_learning/project/image-service/app/infrastructure/integrations/inversion)
- [`Поворот изображения`](machine_learning/project/image-service/app/infrastructure/integrations/rotation)
- [`Стилизация первого изображения по стилю второго`](machine_learning/project/image-service/app/infrastructure/integrations/stylization)
