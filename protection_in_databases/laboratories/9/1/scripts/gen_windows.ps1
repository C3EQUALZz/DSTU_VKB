# Значения по умолчанию
$COUNTRY = 'US'
$STATE = 'California'
$LOCATION = 'Santa Clara'
$BLOCK_SIZE = 4096
$DAYS = 365

# Запрашиваем параметры у пользователя
$REPLY = Read-Host "Enter country code [empty for default value - US]"
if ($REPLY) { $COUNTRY = $REPLY }

$REPLY = Read-Host "Enter state [empty for default value - California]"
if ($REPLY) { $STATE = $REPLY }

$REPLY = Read-Host "Enter location [empty for default value - Santa Clara]"
if ($REPLY) { $LOCATION = $REPLY }

$REPLY = Read-Host "Enter block size [empty for default value - 4096]"
if ($REPLY) { $BLOCK_SIZE = [int]$REPLY }

$REPLY = Read-Host "Enter expiration length [empty for default value - 365]"
if ($REPLY) { $DAYS = [int]$REPLY }

# Формируем строки для openssl
$OPENSSL_SUBJ = "/C=$COUNTRY/ST=$STATE/L=$LOCATION"
$OPENSSL_CA = "$OPENSSL_SUBJ/CN=fake-CA"
$OPENSSL_SERVER = "$OPENSSL_SUBJ/CN=localhost"
$OPENSSL_CLIENT = "$OPENSSL_SUBJ/CN=fake-client"

# Создаем директорию
New-Item -Path "certs" -ItemType Directory -Force | Out-Null

# Функция проверки успешного выполнения команд
function Check-OpenSSLError {
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Ошибка при выполнении команды OpenSSL. Остановка скрипта."
        Exit 1
    }
}

# Генерируем корневой CA сертификат
Write-Host "Генерация CA-ключа..."
openssl genrsa -out certs\ca-key.pem $BLOCK_SIZE
Check-OpenSSLError

# Конвертируем в старый формат
openssl rsa -in certs\ca-key.pem -out certs\ca-key.pem
Check-OpenSSLError

openssl req -new -x509 -nodes -days $DAYS `
    -subj "$OPENSSL_CA" `
    -key certs\ca-key.pem -out certs\ca.pem
Check-OpenSSLError

# Создаем серверные сертификаты
Write-Host "Генерация серверных сертификатов..."
openssl req -newkey rsa:$BLOCK_SIZE -nodes `
    -subj "$OPENSSL_SERVER" `
    -addext "subjectAltName = DNS:localhost, DNS:postgres, IP:127.0.0.1" `
    -keyout certs\server-key.pem -out certs\server-req.pem
Check-OpenSSLError

# Конвертируем в старый формат
openssl rsa -in certs\server-key.pem -out certs\server-key.pem
Check-OpenSSLError

# Создаем конфиг для SAN
$SAN_CONFIG = @"
[req]
req_extensions = v3_req

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = postgres
IP.1 = 127.0.0.1
"@
$SAN_CONFIG | Out-File -FilePath san.cnf -Encoding ASCII

# Подписываем сертификат с SAN
openssl x509 -req -in certs\server-req.pem -days $DAYS `
    -CA certs\ca.pem -CAkey certs\ca-key.pem -CAcreateserial `
    -out certs\server-cert.pem -extensions v3_req -extfile san.cnf
Check-OpenSSLError

# Удаляем временный файл
Remove-Item san.cnf -ErrorAction SilentlyContinue

# Создаем клиентские сертификаты
Write-Host "Генерация клиентских сертификатов..."
openssl req -newkey rsa:$BLOCK_SIZE -nodes `
    -subj "$OPENSSL_CLIENT" `
    -keyout certs\client-key.pem -out certs\client-req.pem
Check-OpenSSLError

# Конвертируем в старый формат
openssl rsa -in certs\client-key.pem -out certs\client-key.pem
Check-OpenSSLError

openssl x509 -req -in certs\client-req.pem -days $DAYS `
    -CA certs\ca.pem -CAkey certs\ca-key.pem -CAcreateserial `
    -out certs\client-cert.pem
Check-OpenSSLError

# Проверяем сертификаты
Write-Host "Проверка сертификатов..."
openssl verify -CAfile certs\ca.pem certs\server-cert.pem certs\client-cert.pem
Check-OpenSSLError

# Вывод завершения
Write-Host "Сертификаты успешно созданы в директории certs/"