# Лабораторная работа №1. Знакомство с HTML

**Дисциплина:** Разработка защищённых WEB-ресурсов
**Тема:** базовые теги и структура HTML5.

## Цель работы

Ознакомиться с работой тегов и параметров `html`, `head`, `title`, `body`,
`p`, `b`, `em`, `u`, `i`, `font`, `ol`/`ul`, `li`, `a` и других;
научиться создавать корректный HTML-документ, оформлять текст, списки,
ссылки, изображения, таблицы, формы; познакомиться с семантической
разметкой HTML5, встраиванием медиа и iframe.

## Состав работы (11 заданий)

| № | Файл | Что демонстрируется | Использованные теги |
|---|------|----------------------|---------------------|
| 1 | [`01-simple-page.html`](01-simple-page.html) | Простая страница | `h1`, `p`, `hr`, `title` |
| 2 | [`02-text-formatting.html`](02-text-formatting.html) | Форматирование текста | `b`, `strong`, `i`, `em`, `u`, `small`, `mark`, `del`, `ins`, `sub`, `sup` |
| 3 | [`03-lists.html`](03-lists.html) | Списки | `ul`, `ol`, `li`, вложенные, `type` |
| 4 | [`04-links.html`](04-links.html) | Ссылки | `a` с `href`, `target="_blank"`, якорь `#id`, `download` |
| 5 | [`05-images.html`](05-images.html) | Изображения | `img` с `src`, `alt`, `width`, `height`, `title`, изображение-ссылка |
| 6 | [`06-tables.html`](06-tables.html) | Таблицы | `table`, `caption`, `thead`/`tbody`, `tr`, `th`, `td`, `colspan`, `rowspan` |
| 7 | [`07-input-types.html`](07-input-types.html) | Тег `input` — все типы | 23 варианта `type` |
| 8 | [`08-forms.html`](08-forms.html) | Формы | `form`, `fieldset`, `legend`, `label`, `input`, `textarea`, `select`, `option`, `button`, чекбоксы, радио, `range`, `date`, `password` |
| 9 | [`09-semantic.html`](09-semantic.html) | Семантическая структура | `header`, `nav`, `main`, `article`, `aside`, `footer` |
| 10 | [`10-audio-video.html`](10-audio-video.html) | Аудио и видео | `audio`, `video`, `source`, `iframe` (YouTube, Vimeo) |
| 11 | [`11-iframe.html`](11-iframe.html) | Встраивание Google Maps | `iframe` |

Точкой входа служит [`index.html`](index.html) — со ссылками на все
11 страниц.

## Структура каталога

```
1/
├── ЛР1.pdf                          ← оригинал задания
├── README.md                        ← этот файл
├── index.html                       ← содержание со ссылками
├── 01-simple-page.html
├── 02-text-formatting.html
├── 03-lists.html
├── 04-links.html
├── 05-images.html
├── 06-tables.html
├── 07-input-types.html
├── 08-forms.html
├── 09-semantic.html
├── 10-audio-video.html
├── 11-iframe.html
└── assets/
    ├── chrome.svg                   ← SVG-логотип для заданий с изображениями
    └── example.pdf                  ← минимальный PDF для ссылки-скачивания
```

## Краткая теория: базовый HTML-документ

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Заголовок страницы</title>
</head>
<body>
    <h1>Заголовок</h1>
    <p>Параграф</p>
</body>
</html>
```

| Тег | Описание |
|-----|----------|
| `<!DOCTYPE html>` | Инструкция для браузера: используется HTML5. |
| `<html>` | Корневой элемент. Атрибут `lang` помогает поисковикам и screen-readers. |
| `<head>` | Метаинформация (кодировка, title, viewport, ссылки на CSS). |
| `<title>` | Заголовок вкладки браузера. Единственный обязательный тег внутри `<head>`. |
| `<meta charset>` | Кодировка документа (UTF-8). |
| `<meta name="viewport">` | Адаптация под мобильные устройства. |
| `<body>` | Видимое содержимое страницы. |

W3C рекомендует писать теги в **нижнем регистре** (в XHTML это
обязательно). На всех страницах работы используется именно такая запись.

## Заметки по отдельным заданиям

- **Задание 7** оформлено как полная таблица из примера в PDF: 23 строки
  для всех значений атрибута `type` (включая устаревший `datetime`).
- **Задание 8** включает не только текстовые поля и textarea, но и
  выпадающий список, чекбоксы, радиокнопки, range, date, password,
  submit/reset — как в примере результата.
- **Задание 9** реализует структуру с шапкой, навигацией, основной
  областью (article + aside) и подвалом, как на скриншоте в PDF.
- **Задание 10** содержит как локальные плейсхолдеры `<audio>`/`<video>`
  (если соответствующих медиафайлов нет — браузер просто покажет
  пустой плеер, контролы доступны), так и iframe с YouTube и Vimeo.
- **Задание 11** использует публичный embed-URL Google Maps без
  API-ключа (через `maps.google.com/maps?q=...&output=embed`) —
  встраивание работает напрямую с `file://`, без локального сервера.

## Как запустить

### Способ 1. Двойной клик
Достаточно открыть `index.html` в любом современном браузере
(Chrome, Firefox, Edge, Safari). Все ссылки между страницами работают.

### Способ 2. Локальный HTTP-сервер
Некоторые встроенные виджеты (например, embed YouTube/Vimeo и Google
Maps) корректнее работают по HTTP, чем по `file://`. Запустите из этой
папки:

```bash
python3 -m http.server 8000
```

И откройте <http://localhost:8000/> в браузере.

## Проверка корректности

После создания файлов выполнялась проверка локальным сервером:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 &
for f in index 01-simple-page 02-text-formatting 03-lists 04-links \
         05-images 06-tables 07-input-types 08-forms 09-semantic \
         10-audio-video 11-iframe; do
    curl -s -o /dev/null -w "%{http_code} $f.html\n" \
         "http://127.0.0.1:8765/$f.html"
done
```

Все 12 страниц возвращают `200 OK`.

## Выводы

В рамках работы созданы 11 самостоятельных HTML-страниц, каждая из
которых демонстрирует одну тему из списка изучаемых тегов. Все
страницы — валидные документы HTML5 с указанной кодировкой UTF-8,
языком `ru`, `viewport`-метатегом и заголовком вкладки. Реализованы
все 11 пунктов рабочего задания. Точка входа `index.html` собирает
их в единый набор, удобный для просмотра и защиты.
