## 7) С помощью PowerShell получить для просмотра и изменения настроек BIOS на ПК, например, включить/отключить загрузку компьютера с USB устройств

- Вывод информации по BIOS

```
Get-CimInstance -Class Win32_BIOS
```

- Полный список параметров BIOS, который доступен в WMI классе Win32_BIOS

```
Get-WmiObject -Class Win32_BIOS | Format-List *
```

- Можно вывести интересующие параметры

```
Get-WmiObject -Class Win32_BIOS | Select SMBIOSBIOSVersion, Manufacturer, SerialNumber, ReleaseDate
```


