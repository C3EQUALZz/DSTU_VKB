# Лабораторная работа №3. Адаптивная вёрстка

**Дисциплина:** Разработка защищённых WEB-ресурсов
**Тема:** подключение стилей, CSS Grid и Flexbox, Media Queries,
относительные единицы, mobile-first.

## Цель работы

Сформировать понимание основных способов подключения CSS-стилей и
научиться применять CSS для адаптивной стилизации HTML-элементов.
Освоить Media Queries, гибкие макеты на относительных единицах,
viewport meta tag, оптимизацию изображений.

## Краткая теория

### Базовый набор для адаптива

1. **Viewport** — без него мобильный браузер «расфокусируется»:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1">
   ```
2. **Относительные единицы**: `%`, `em`, `rem`, `vw`, `vh`, `fr`,
   `minmax(...)`. Они растягиваются под размер контейнера/шрифта.
3. **Media Queries**: `@media (min-width: 768px) { ... }`
   — стиль применяется только при подходящей ширине окна.
4. **Mobile-first**: базовые правила — для мобильных,
   `@media (min-width: ...)` — расширения для более широких экранов.
   Это короче и проще, чем «desktop-first» + `max-width`.

### Flexbox vs Grid

| Когда нужен | Используем |
|-------------|------------|
| Один ряд / одна колонка элементов, выравнивание | **Flexbox** |
| Двумерная сетка (карточки, лендинг) | **Grid** |
| Часто — комбинация: Grid для общего макета, Flex внутри карточек | оба |

### CSS-только переключатели без JavaScript

В заданиях 2 и 6 раскрытие меню/панели фильтров реализовано через
скрытый `<input type="checkbox">` и селектор `:checked`:

```html
<input type="checkbox" id="menu-toggle" hidden>
<label for="menu-toggle">≡ Меню</label>
<nav>...</nav>
```

```css
#menu-toggle:checked ~ nav { max-height: 400px; }
```

## Состав работы (7 заданий)

### Задание 1. Адаптивная сетка товаров (Grid)

[`01-grid-products.html`](01-grid-products.html) + [`css/01-grid-products.css`](css/01-grid-products.css).
12 карточек товаров. Брейкпоинты:
- `<768px` → 2 в строке;
- `768–1199px` → 3 в строке;
- `≥1200px` → 4 в строке.

Базовый CSS — mobile-first (`grid-template-columns: repeat(2, 1fr)`),
расширение через `@media (min-width: 768px)` и `(min-width: 1200px)`.

### Задание 2. Sticky-header + гамбургер без JavaScript

[`02-sticky-menu.html`](02-sticky-menu.html) + [`css/02-sticky-menu.css`](css/02-sticky-menu.css).
- `position: sticky; top: 0;` на хедере.
- На мобильных (`max-width: 767px`) ссылки сворачиваются в выпадающий
  список под иконкой-«бургер».
- Переключение — **только CSS**: `<input type="checkbox" id="menu-toggle">`
  + селектор `.menu-toggle:checked ~ .header .nav { max-height: 400px; }`.

### Задание 3. Адаптивная форма «Обратная связь»

[`03-contact-form.html`](03-contact-form.html) + [`css/03-contact-form.css`](css/03-contact-form.css).
- Поля «Имя» и «Email» — в одной строке при `≥768px`, в столбец на
  мобильных. Реализовано через CSS Grid: `grid-template-columns: 1fr`
  по умолчанию, `1fr 1fr` в медиа-запросе.
- Валидация — нативная HTML5 (`required`, `type="email"`).

### Задание 4. Адаптивный «О компании» (Flexbox)

[`04-company-info.html`](04-company-info.html) + [`css/04-company-info.css`](css/04-company-info.css).
- На десктопе — `flex-direction: row` (лого слева, текст справа).
- На мобильных — `flex-direction: column` (лого сверху, текст снизу).
- Логотип — inline SVG с градиентом.

### Задание 5. Адаптивная таблица (Stack Table)

[`05-stack-table.html`](05-stack-table.html) + [`css/05-stack-table.css`](css/05-stack-table.css).
- На десктопе — стандартная таблица.
- На `<768px` каждая строка превращается в карточку: `thead` скрыт,
  ячейки получают подписи через `data-label` + `content: attr(data-label)`
  на псевдоэлементе `::before`.

### Задание 6. Адаптивные фильтры результатов (CSS-only)

[`06-filters.html`](06-filters.html) + [`css/06-filters.css`](css/06-filters.css).
- На десктопе — двухколоночный макет: фильтры слева, результаты справа.
- На `<800px` фильтры скрываются, появляется кнопка «Показать фильтры».
- Раскрытие — снова через `<input type="checkbox">` + `:checked`. **Без JS.**

### Задание 7. Landing Page

[`07-landing.html`](07-landing.html) + [`css/07-landing.css`](css/07-landing.css).
- Sticky-header с навигацией и логотипом.
- Hero c CTA-кнопкой (`clamp()` для адаптивного шрифта).
- 3 карточки преимуществ (`grid-template-columns: 1fr` → `repeat(3, 1fr)`).
- 3 тарифа с выделенным центральным (`scale(1.04)` + рамка).
- «Карусель» отзывов на горизонтальном Flexbox + `scroll-snap`.
- Форма «Связаться с нами» (на узких экранах поля становятся в столбец).
- Тёмный футер.

## Структура файлов

```
3/
├── ЛР3.pdf
├── README.md
├── index.html                              ← содержание
├── 01-grid-products.html
├── 02-sticky-menu.html
├── 03-contact-form.html
├── 04-company-info.html
├── 05-stack-table.html
├── 06-filters.html
├── 07-landing.html
└── css/
    ├── reset.css                           ← переменные + сброс
    ├── 01-grid-products.css
    ├── 02-sticky-menu.css
    ├── 03-contact-form.css
    ├── 04-company-info.css
    ├── 05-stack-table.css
    ├── 06-filters.css
    └── 07-landing.css
```

## Как запустить

```bash
cd development_of_secure_web_resources/2025/3
python3 -m http.server 8000
```

Открыть <http://localhost:8000/>. Для проверки адаптива:
DevTools → Toggle device toolbar (или просто менять ширину окна).

## Проверка (выполнялась)

```bash
python3 -m http.server 8767 --bind 127.0.0.1 &
for f in index 01-grid-products 02-sticky-menu 03-contact-form \
         04-company-info 05-stack-table 06-filters 07-landing; do
    curl -s -o /dev/null -w "%{http_code} $f.html\n" \
         http://127.0.0.1:8767/$f.html
done
```
Все 8 страниц и 8 CSS-файлов возвращают `200 OK`.

Также проверено, что в `css/02-sticky-menu.css` и `css/06-filters.css`
**нет** JavaScript — переключение реализовано чистым CSS через
`:checked`.

## Выводы

В работе использованы основные техники адаптивной вёрстки:
viewport-метатег, mobile-first медиа-запросы, CSS Grid для двумерных
сеток, Flexbox для одномерных компоновок, `position: sticky`,
`scroll-snap` для каруселей, `:checked`-переключатели без JavaScript,
адаптивная таблица через `data-label` + `::before`. Все 7 задач
проходят базовую проверку 200 OK.
