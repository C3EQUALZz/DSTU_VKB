## Выполнить индивидуальные задания для студентов согласно (табл. 6).

- нахождения среди выполняющихся процессов имен процессов с наименьшим значением BasePriority

```
# Получаем список всех процессов
$processes = Get-Process

# Находим минимальное значение BasePriority среди всех процессов
$minBasePriority = $processes | Measure-Object BasePriority -Minimum | Select-Object -ExpandProperty Minimum

# Находим процессы с минимальным значением BasePriority
$minPriorityProcesses = $processes | Where-Object { $_.BasePriority -eq $minBasePriority }

# Выводим имена процессов с наименьшим значением BasePriority
Write-Host "Процессы с наименьшим значением BasePriority ($minBasePriority):"
$minPriorityProcesses | Select-Object ProcessName, BasePriority | Format-Table -AutoSize
```

- нахождения среди выполняющихся процессов имен процессов, у которых значения параметра WorkingSet одинаковы

```
# Получаем список всех процессов
$processes = Get-Process

# Группируем процессы по значению WorkingSet64 (размер рабочей области процесса)
$groupedProcesses = $processes | Group-Object WorkingSet64 | Where-Object { $_.Count -gt 1 }

# Выводим группы процессов с одинаковым значением WorkingSet
Write-Host "Процессы с одинаковым значением WorkingSet (в байтах):"
foreach ($group in $groupedProcesses) {
    Write-Host "WorkingSet = $($group.Name):"
    $group.Group | Select-Object ProcessName, Id, WorkingSet64 | Format-Table -AutoSize
    Write-Host "`n"
}
```