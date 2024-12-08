## Cоздать текстовый файл, содержащий список выполняемых процессов, упорядоченный по возрастанию указанного в табл. 5 параметра. Имена параметров процессов указаны так же в табл. 5.

- Список выводимых параметров процессов: Имя процесса, Id, PriorityClass, UserprocessorTime, TotalProcessorTime
- Сортировать по значению параметра: TotalProcessorTime
- Вывести процессы, у которых: Id > 100

```
Get-Process | Where-Object {$_.Id -gt 100} | Sort-Object TotalProcessorTime | Select-Object ProcessName, Id, PriorityClass, UserProcessorTime, TotalProcessorTime | Out-File -FilePath D:\PycharmProjects\DSTU_VKB\operation_systems\fith_semester\2_laboratory\4_question\3_and_5_variant\processes.txt 
```
