## Вывести значения нескольких системных счетчиков через каждые 3 секунды с помощью команды sar

Команда sar (System Activity Reporter) используется для мониторинга различных системных параметров,
таких как использование CPU, памяти, дискового ввода-вывода и сетевого трафика.
Чтобы вывести значения нескольких системных счетчиков через каждые 3 секунды, можно использовать команду
sar с соответствующими параметрами.

```bash
sar 3 5
```

В нашем примере команда `sar 3 5` выводит значения системных счетчиков каждые 3 секунды и делает это 5 раз.
