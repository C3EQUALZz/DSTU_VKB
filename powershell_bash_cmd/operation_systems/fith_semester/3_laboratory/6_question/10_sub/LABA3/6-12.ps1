#Получить список служб и их состояние: 
Get-Service
#Вывести имя, статус и доступные возможности любой службы:
Get-Service -Name "Wsearch"
#Вывести службы, необходимые для запуска текущей службы: 
Get-Service "Wsearch" | Select-Object -ExpandProperty DependentServices
#Вывести зависимые службы от текущей:
Get-Service "Wsearch" | Select-Object -ExpandProperty ServicesDependedon
#проверить, что в системе имеется указанная служба: 
Get-Service -Name "Wsearch"
#Остановить любую службу, включая зависимые:
Stop-Service -Name "Wsearch" -Force
#Запустить любую службу, включая зависимые: 
Start-Service -Name "Wsearch" 
#Отобразить список всех служб, работа которых может быть приостановлена: 
Get-Service | Where-Object { S_.CanPauseAndContinue -eq $true }
#Приостановить любую службу и возобновить ее работу:
Suspend-Service -Name "Wsearch"
Resume-Service -Name "Wsearch"
#изменить тип запуска службы - ручной, автоматический: 
Set-Service -Name "Wsearch" -StartupType Automatic
Set-Service -Name "Wsearch" -StartupType Manual 
#Создать новую службу Testservice в Windows:
New-Service -Name "TestService" -BinaryPathName "C:\sluzba.exe"
#Получить информацию о режиме запуска и описание службы:
Get-WmiObject Win32_Service -Filter "Name='TestService'" | Select-Object StartMode, Description
#получить имя учетной записи, которая используется для запуска службы Testservice: 
Get-WmiObject Win32_Service -Filter "Name='TestService'" | Select-Object StartName 
#изменить имя и пароль учетной записи указанной службы: 
Set-Service -Name "TestService" -UserName "Oleg" -Password "1234" 
#Удалить службу: 
Get-Service -Name "TestService" | Stop-Service -Force
Get-WmiObject Win32_Service -Filter "Name='TestService'" | Invoke-WmiMethod -Name Delete