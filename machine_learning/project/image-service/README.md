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

Каждая обработка происходит в фоновой задаче и при успехе отправляется в брокер сообщения в нужный топик.

> [!NOTE]
> Если хотите добавить новый функционал по обработке изображения, то вам нужно добавить некоторые абстракции в виде команд, ивентов, джобов и т.п. Посмотрите на исходный код, вам станет понятно)

### Полезные ссылки

- [`Настройка Gunicorn`](https://adamj.eu/tech/2021/12/29/set-up-a-gunicorn-configuration-file-and-test-it/)