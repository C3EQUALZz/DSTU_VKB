## Вывести содержимое указанного в табл.6 каталога по указанному формату на экран и в файл.

- Имя каталога: %Windows% и все подкаталоги
- Что выводить: Только файлы bmp
- Сортировать по: размеру
- Атрибуты файлов и каталогов: только чтение

```
DIR %WINDIR%\*.bmp /S /A:R /O:S > output.txt & TYPE output.txt
```

### Объяснения

- `%WINDIR%` — переменная окружения, указывающая на каталог Windows.
- `*.bmp` — фильтр для поиска файлов с расширением .bmp.
- `/S` — рекурсивный поиск в подкаталогах.
- `/A:R` — отображение только файлов с атрибутом "только для чтения".
- `/O:S` — сортировка по размеру (от меньшего к большему).
- `> output.txt` — перенаправление вывода в указанный файл.
