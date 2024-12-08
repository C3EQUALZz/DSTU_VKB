## 12) Управление службами Windows с помощью PowerShell:
- получить список служб и их состояние

```
Get-Service
```

- вывести имя, статус и доступные возможности любой службы

В вашем случае поменяйте имя службы на другое, которое захотите

```
Get-Service -Name "Redis" | Select-Object Name, Status, DisplayName
```

- вывести службы, необходимые для запуска текущей службы

```
Get-Service -Name "Redis" | Select-Object -ExpandProperty DependentServices
```

- вывести зависимые службы от текущей

```
Get-Service -Name "Redis" | Select-Object -ExpandProperty ServicesDependedOn
```

- проверить, что в системе имеется указанная служба,

```
Get-Service -Name "Redis" -ErrorAction SilentlyContinue
```

- остановите любую службу, включая зависимые,

```
Stop-Service -Name "Redis" -Force
```

- запустите любую службу, включая зависимые

```
Start-Service -Name "Redis"
```

- отобразите список всех служб, работа которых может быть приостановлена

```
Get-Service | Where-Object { $_.CanPauseAndContinue -eq $true }
```

- приостановите любую службу и возобновите ее работу

```
Suspend-Service -Name "Redis"
Resume-Service -Name "Redis"
```

- измените тип запуска службы – ручной, автоматический,

```
Set-Service -Name "Redis" -StartupType Manual
Set-Service -Name "Redis" -StartupType Automatic
```

- создайте новую службу TestService в Windows. Для новой службы требуется
указать имя и исполняемый файл,

```
New-Service -Name "TestService" -DisplayName "Test Service" -BinaryPathName "D:\DOSBox\DOSBox-0.74\DOSBox.exe" -StartupType Manual
```

- получите информацию о режиме запуска и описание службы

```
Get-Service -Name "ИмяСлужбы" | Select-Object StartType, Description
```

- получите имя учетной записи, которая используется для запуска службы
TestService,

```
Get-WmiObject -Class Win32_Service -Filter "Name='TestService'" | Select-Object StartName
```

- изменените имени и пароль учетной записи указанной службы
- 
```
$service = Get-WmiObject -Class Win32_Service -Filter "Name='ИмяСлужбы'"
$service.Change("ИмяУчетнойЗаписи", "Пароль")
```

- удалите службу.

```
Remove-Service -Name "TestService"
```

