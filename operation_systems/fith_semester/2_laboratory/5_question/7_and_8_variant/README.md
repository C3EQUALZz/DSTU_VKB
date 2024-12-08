## Cоздать HTML-файл, содержащий список выполняемых процессов, упорядоченный по возрастанию указанного в табл. 5 параметра. Имена параметров процессов указаны так же в табл. 5.

- Список выводимых параметров процессов: Имя процесса, PriorityClass, ProductVersion, Id
- Сортировать по значению параметра: Имя процесса
- Вывести процессы, у которых: Id > 100

```
# Получаем список процессов и фильтруем по Id > 100
$processes = Get-Process | Where-Object { $_.Id -gt 100 }

# Формируем список с нужными параметрами: Имя процесса, PriorityClass, ProductVersion, Id
$formattedProcesses = $processes | Select-Object `
    @{Name="Process Name";Expression={$_.ProcessName}}, `
    @{Name="PriorityClass";Expression={try { $_.PriorityClass } catch { "N/A" }}}, `
    @{Name="ProductVersion";Expression={try { $_.MainModule.FileVersionInfo.ProductVersion } catch { "N/A" }}}, `
    Id

# Сортируем список по имени процесса
$sortedProcesses = $formattedProcesses | Sort-Object "Process Name"

# Начинаем формирование HTML-контента
$html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Process List</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h2>Process List (Id > 100, sorted by Process Name)</h2>
    <table>
        <tr>
            <th>Process Name</th>
            <th>Priority Class</th>
            <th>Product Version</th>
            <th>Process Id</th>
        </tr>
"@

# Формируем строки для каждой записи процесса
foreach ($process in $sortedProcesses) {
    $html += "<tr>"
    $html += "<td>" + $process."Process Name" + "</td>"
    $html += "<td>" + $process.PriorityClass + "</td>"
    $html += "<td>" + $process.ProductVersion + "</td>"
    $html += "<td>" + $process.Id + "</td>"
    $html += "</tr>"
}

# Заканчиваем HTML
$html += @"
    </table>
</body>
</html>
"@

# Записываем HTML в файл
$html | tee "D:\PycharmProjects\DSTU_VKB\operation_systems\fith_semester\2_laboratory\5_question\7_and_8_variant\process_list.html"

# Открываем HTML файл в браузере для проверки (опционально)
Start-Process "D:\PycharmProjects\DSTU_VKB\operation_systems\fith_semester\2_laboratory\5_question\7_and_8_variant\process_list.html"
```