                                                                                                                             # Параметры задачи
$taskName = "RunPowerShellScriptAtSpecificTime"
$taskDescription = "This task runs a PowerShell script at a specific time."
$taskAction = "powershell.exe"
$taskArguments = "-File D:\PycharmProjects\DSTU_VKB\operation_systems\1\3_laboratory\6_question\2_sub\hello.ps1"
$taskTriggerTime = "2024-09-25T15:29:00"  # Укажите время запуска задачи

# Создание новой задачи
$action = New-ScheduledTaskAction -Execute $taskAction -Argument $taskArguments
$trigger = New-ScheduledTaskTrigger -Once -At $taskTriggerTime
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Регистрация задачи
Register-ScheduledTask -TaskName $taskName -Description $taskDescription -Action $action -Trigger $trigger -Principal $principal -Settings $settings

# Экспорт задачи в XML-файл
$taskPath = "C:\Windows\System32\Tasks\$taskName"
$xmlFilePath = "D:\PycharmProjects\DSTU_VKB\operation_systems\1\3_laboratory\6_question\2_sub\ExportedTask.xml"
schtasks /query /tn $taskName /xml > $xmlFilePath
