## Вывести содержимое каталога Windows (для вариантов 5 и 10 – и подкаталогов) по указанному в табл. 4 формату на экран и в текстовый файл.

- Что выводить (имена, размер, дата создания, атрибуты): Файлы и подкаталоги
- Сортировать по: По дате
- Условие отбора: Первые буквы имени SY

Важно поменяйте путь на результирующий файл на ваше расположение, посмотрите на путь правее от tee. 

```
# Путь к каталогу Windows
$path = $env:WINDIR

# Используем ls как алиас Get-ChildItem, фильтруем файлы и каталоги по имени
$items = ls -Recurse -ErrorAction SilentlyContinue $path | Where-Object { $_.Name -like "SY*" } | Sort-Object LastWriteTime

# Форматируем вывод как таблицу: имя, размер, дата изменения, атрибуты
$formattedItems = $items | Select-Object Name, @{Name="Size (Bytes)";Expression={if ($_.PSIsContainer) { "-" } else { $_.Length }}}, @{Name="Date Modified";Expression={$_.LastWriteTime}}, Attributes

# Выводим результат на экран
$formattedItems | Format-Table -AutoSize

# Записываем результат в текстовый файл
$formattedItems | tee "D:\PycharmProjects\DSTU_VKB\operation_systems\fith_semester\2_laboratory\2_question\2_and_7_variant\result.txt"
```

Объяснение: 
- ls аллиас из Unix-подобных систем, чтобы просмотреть все элементы в файле
- $env:WINDIR - это более надежный способ получить путь к каталогу Windows в PowerShell.
- `-Recurse` - это рекурсивный поиск директорий
- `-Force` - это поиск, учитывая скрытые файлы
- `-ErrorAction SilentlyContinue` - это игнорировать ошибок по разрешимости и доступности 