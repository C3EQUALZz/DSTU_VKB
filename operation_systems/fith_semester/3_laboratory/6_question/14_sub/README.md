## 14) Создайте самоподписанный сертификат в PowerShell и импортируйте его в персональное хранилище компьютера. Можно использовать командлет New-SelfSignedCertificate, входящий в состав модуля PKI (Public Key Infrastructure). С помощью командлета Get-ChildItem можно вывести все параметры созданного сертификата по его отпечатку (Thumbprint). Задать срок действия сертификата – 3 года. Ключ сертификата или сам файл сертификата подготовить для распостранения на все ПК.

> [!NOTE] 
> Примечание. Самоподписанные сертификаты рекомендуется использовать в
> тестовых целях или для обеспечения сертификатами внутренних интранет служб.

Запускайте PowerShell от имени администратора

```
$cert = New-SelfSignedCertificate -Subject "Cert for laba” -CertStoreLocation "cert:\LocalMachine\My" -NotAfter (Get-Date).AddYears(3)
```

```
Get-ChildItem -Path "cert:\LocalMachine\My" | Where-Object { $_.Thumbprint -eq $cert.Thumbprint }
```