## 13) Отправить письмо с указанной темой и вложением из скрипта PS. Использовать для письма кодировку UTF8

# Укажите параметры

```
$smtpServer = "smtp.gmail.com"  # Замените на ваш SMTP-сервер
$smtpPort = 587                  # Замените на нужный порт
$from = ""   # Ваш email
$to = ""  # Email получателя
$subject = "Теcт лабы"
$body = "<h1>Привет мир!</h1>"
$username = ""  # Ваш email для аутентификации
$password = ""          # Ваш пароль

# Создание объекта для аутентификации
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($username, $securePassword)

# Создание объекта SmtpClient
$smtpClient = New-Object System.Net.Mail.SmtpClient($smtpServer, $smtpPort)
$smtpClient.EnableSsl = $true
$smtpClient.Credentials = $credential

# Создание сообщения
$mailMessage = New-Object System.Net.Mail.MailMessage
$mailMessage.From = $from
$mailMessage.To.Add($to)
$mailMessage.Subject = $subject
$mailMessage.Body = $body
$mailMessage.BodyEncoding = [System.Text.Encoding]::UTF8  # Установка кодировки UTF-8
$mailMessage.SubjectEncoding = [System.Text.Encoding]::UTF8  # Установка кодировки для темы

# Отправка сообщения
$smtpClient.Send($mailMessage)

# Освобождение ресурсов
$mailMessage.Dispose()
$smtpClient.Dispose()
```
