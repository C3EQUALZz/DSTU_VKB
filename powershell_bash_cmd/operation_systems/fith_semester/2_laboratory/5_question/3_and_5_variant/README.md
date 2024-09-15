## Cоздать HTML-файл, содержащий список выполняемых процессов, упорядоченный по возрастанию указанного в табл.5 параметра. Имена параметров процессов указаны в табл. 5.

- Список выводимых параметров процессов: Имя процесса, Id, PriorityClass, UserprocessorTime, TotalProcessorTime
- Сортировать по значению параметра: TotalProcessorTime
- Вывести процессы, у которых: Id > 100

```
Get-Process | Where-Object {$_.Id -gt 100} | Sort-Object TotalProcessorTime | Select-Object ProcessName, Id, PriorityClass, UserProcessorTime, TotalProcessorTime | Out-File -FilePath processes.html
```

Объяснение: 

Сделал аналагично, как в 4 задании, но выгружал уже в html файл (тут снизу можно создать переменную для html, провести редактирование в html(<html><head>.......<html>), тем самым создать что-то типо красивого оформеления, но я не запаривался, так как плохо выводятся данные в таком случае
