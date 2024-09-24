## 15) Создать самоподписанный сертификат для подписывания кода приложений, проверить доверенность сертификата, настроить и подписать им скрипт PS.

### Создаем сертификат с помощью Powershell

> [!IMPORTANT]
> Открывайте Powershell от имени администратора

Используем командлет `New-SelfSignedCertificate` для создания самоподписанного сертификата.
```
$cert = New-SelfSignedCertificate -Subject "Cert for Code Signing” -Type CodeSigningCert -CertStoreLocation cert:\LocalMachine\My
```

### Подписываем скрипт

Для вашего варианта поменяйте путь к проекту

```
$scriptPath = "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\15_sub\StartScript.ps1"
Set-AuthenticodeSignature -FilePath $scriptPath -Certificate $cert
```

### Проверка подписи

```
Get-AuthenticodeSignature -FilePath $scriptPath
```

Если при выполнении команды появится предупреждение UnknownError, значит этот сертификат недоверенный,
т.к. находится в персональном хранилище сертификатов пользователя


