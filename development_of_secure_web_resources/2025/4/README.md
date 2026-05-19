# Лабораторная работа №4. Ветвящиеся и циклические алгоритмы в JS

**Дисциплина:** Разработка защищённых WEB-ресурсов
**Тема:** условные конструкции и циклы в JavaScript.

## Цель работы

Получить практические навыки применения синтаксиса JavaScript для
реализации ветвящихся (условных) и циклических алгоритмов; оценить
применимость различных подходов к решению типовых задач.

## Краткая теория

### Условные конструкции

- **`if / else if / else`** — стандартная цепочка (задачи 1, 4, 8).
- **`switch (value) { case ... }`** — удобно для дискретных значений.
- **Тернарный оператор** — `cond ? a : b` (короткая форма if/else).
- **Логические операторы** `&&`, `||`, `!` — комбинируют условия.

### Циклы

| Конструкция | Когда удобна |
|-------------|--------------|
| `for (let i = 0; i < n; i++)` | классический счётный цикл (задачи 2, 5, 6, 9) |
| `while (cond)` | пока условие истинно (задача 7) |
| `do { } while (cond)` | хотя бы один проход |
| `for (const x of arr)` | перебор массива/строки по элементам (задачи 3, 10) |
| `for (const k in obj)` | перебор ключей объекта |

Операторы управления `break` (выход из цикла) и `continue` (следующая
итерация) дополняют любую из этих конструкций.

### Ввод-вывод

В этой лабе по требованию задания используется:
- ввод — `prompt('...')` (возвращает строку или `null` при отмене);
- вывод — `element.textContent` / `innerHTML` в контейнер `<div>`/`<pre>` с `id="output"`.

Обращений к `alert` и `console.log` нет — это часть оценки лабы.

## Состав работы (10 задач)

| № | Задача | Файлы | Использованные конструкции |
|---|--------|-------|-----------------------------|
| 1  | Оценка погоды для одежды | [`task01.html`](tasks/task01.html) / [`task01-weather.js`](js/task01-weather.js) | `if / else if / else` |
| 2  | Количество чётных чисел | [`task02.html`](tasks/task02.html) / [`task02-evens.js`](js/task02-evens.js) | `for`, `if`, `String.split`, `Number` |
| 3  | Сумма положительных | [`task03.html`](tasks/task03.html) / [`task03-sum-positive.js`](js/task03-sum-positive.js) | `for...of`, `if`, regexp `split` |
| 4  | Угадай число (1…10) | [`task04.html`](tasks/task04.html) / [`task04-guess.js`](js/task04-guess.js) | `if / else if / else`, `Number.isInteger` |
| 5  | Поиск максимума | [`task05.html`](tasks/task05.html) / [`task05-max.js`](js/task05-max.js) | счётный `for`, инициализация максимума |
| 6  | Слова длиной ≥5 | [`task06.html`](tasks/task06.html) / [`task06-long-words.js`](js/task06-long-words.js) | `for`, `push`, `String.length`, динамический DOM |
| 7  | Делители 3 | [`task07.html`](tasks/task07.html) / [`task07-divisible-3.js`](js/task07-divisible-3.js) | `while`, `%`, `if` |
| 8  | Доступ по возрасту | [`task08.html`](tasks/task08.html) / [`task08-age.js`](js/task08-age.js) | `if / else` |
| 9  | Таблица умножения | [`task09.html`](tasks/task09.html) / [`task09-multiplication.js`](js/task09-multiplication.js) | счётный `for` с `<br>` |
| 10 | Гласные буквы | [`task10.html`](tasks/task10.html) / [`task10-vowels.js`](js/task10-vowels.js) | `for...of`, `String.includes` |

### Особенности реализации

1. **Кнопка «Запустить»**: `prompt` не вызывается на загрузке страницы,
   а только по клику. Это удобно для повторного тестирования и для
   защиты лабораторной у преподавателя (преподаватель сам нажимает
   кнопку и видит обработку входа).
2. **Обработка отмены ввода**: если пользователь нажал «Отмена» в
   `prompt`, `prompt` возвращает `null` — программа корректно выводит
   «Ввод отменён», без падений.
3. **Валидация ввода**: пустая строка и нечисловые значения дают
   осмысленное сообщение об ошибке (красная плашка `output.is-error`).
4. **Изоляция**: каждый JS-файл обёрнут в IIFE
   `(function () { 'use strict'; ... })();` — не засоряет глобальное
   пространство имён.

## Структура файлов

```
4/
├── LR_4_*.pdf
├── README.md
├── index.html                           ← содержание
├── css/
│   └── styles.css                       ← общие стили (карточки, кнопки, output)
├── js/
│   ├── task01-weather.js
│   ├── task02-evens.js
│   ├── task03-sum-positive.js
│   ├── task04-guess.js
│   ├── task05-max.js
│   ├── task06-long-words.js
│   ├── task07-divisible-3.js
│   ├── task08-age.js
│   ├── task09-multiplication.js
│   └── task10-vowels.js
└── tasks/
    ├── task01.html
    ├── task02.html
    ├── task03.html
    ├── task04.html
    ├── task05.html
    ├── task06.html
    ├── task07.html
    ├── task08.html
    ├── task09.html
    └── task10.html
```

## Как запустить

```bash
cd development_of_secure_web_resources/2025/4
python3 -m http.server 8000
```

Открыть <http://localhost:8000/>. С главной страницы — переход к
любой из 10 задач. На странице задачи нажать «Запустить» — появится
окно `prompt` для ввода, результат выведется в блок `output`.

Также можно открыть `index.html` двойным кликом (`prompt` работает и
по протоколу `file://`).

## Проверка (выполнялась)

```bash
python3 -m http.server 8768 --bind 127.0.0.1 &
curl -s -o /dev/null -w "%{http_code} index.html\n" http://127.0.0.1:8768/index.html
for i in 01 02 03 04 05 06 07 08 09 10; do
    curl -s -o /dev/null -w "%{http_code} tasks/task$i.html\n" \
         "http://127.0.0.1:8768/tasks/task$i.html"
done
```

Все 11 страниц и все 10 JS-файлов возвращают `200 OK`.

## Выводы

В работе освоены ветвящиеся конструкции (`if / else if / else`) и
циклические (`for`, `while`, `for-of`). Для каждой из 10 задач
показана минимальная, но безопасная реализация: с проверкой ввода,
понятными сообщениями об ошибках и без побочных эффектов в глобальной
области. Все обработчики навешиваются через `addEventListener` после
загрузки модуля (`defer`).
