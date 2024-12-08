## Cоздать текстовый файл, содержащий список выполняемых процессов, упорядоченный по возрастанию указанного в табл. 5 параметра. Имена параметров процессов указаны так же в табл. 5.

- Список выводимых параметров процессов: Имя процесса, PriorityClass, ProductVersion, Id
- Сортировать по значению параметра: Имя процесса
- Вывести процессы, у которых: Id > 100

```
# Получаем список процессов, фильтруем по ID > 100
$processes = Get-Process | Where-Object { $_.Id -gt 100 }

# Для каждого процесса выводим имя процесса, PriorityClass, ProductVersion, Id
$formattedProcesses = $processes | Select-Object `
    @{Name="Process Name";Expression={$_.ProcessName}}, `
    @{Name="PriorityClass";Expression={try { $_.PriorityClass } catch { "N/A" }}}, `
    @{Name="ProductVersion";Expression={try { $_.MainModule.FileVersionInfo.ProductVersion } catch { "N/A" }}}, `
    Id

# Сортируем по имени процесса
$sortedProcesses = $formattedProcesses | sort "Process Name"

# Выводим результат в файл
$sortedProcesses | tee "D:\PycharmProjects\DSTU_VKB\operation_systems\1\2_laboratory\4_question\7_and_8_variant\result.txt"
```

