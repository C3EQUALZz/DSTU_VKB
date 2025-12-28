# PowerShell скрипт для сравнения времени шифрования алгоритмов DES, DES-EDE, DES3 и RSA
# Использование: .\encryption-comparison.ps1 -InputFile "plain.txt" [-Iterations 5] [-ProviderPath "D:\tools\openssl\OpenSSL-Win64\bin"]

param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,
    
    [Parameter(Mandatory=$false)]
    [int]$Iterations = 5,
    
    [Parameter(Mandatory=$false)]
    [string]$ProviderPath = "D:\tools\openssl\OpenSSL-Win64\bin"
)

# Проверка наличия входного файла
if (-not (Test-Path $InputFile)) {
    Write-Host "Ошибка: Файл '$InputFile' не найден!" -ForegroundColor Red
    exit 1
}

# Проверка размера файла для RSA
$fileSize = (Get-Item $InputFile).Length
if ($fileSize -gt 245) {
    Write-Host "Предупреждение: Файл больше 245 байт. RSA может не работать с файлами больше ~245 байт для 2048-битного ключа." -ForegroundColor Yellow
    Write-Host "Размер файла: $fileSize байт" -ForegroundColor Yellow
}

# Проверка наличия OpenSSL
try {
    $opensslVersion = openssl version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "OpenSSL не найден"
    }
    Write-Host "OpenSSL найден: $opensslVersion" -ForegroundColor Green
} catch {
    Write-Host "Ошибка: OpenSSL не установлен или не доступен в PATH!" -ForegroundColor Red
    exit 1
}

# Получение директории скрипта
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$workDir = if ($scriptDir) { $scriptDir } else { Get-Location }

Write-Host "`n=== Сравнение времени шифрования алгоритмов ===" -ForegroundColor Cyan
Write-Host "Входной файл: $InputFile" -ForegroundColor Yellow
Write-Host "Размер файла: $fileSize байт" -ForegroundColor Yellow
Write-Host "Количество итераций: $Iterations" -ForegroundColor Yellow
Write-Host "Рабочая директория: $workDir" -ForegroundColor Gray

# Функция для измерения времени шифрования
function Measure-EncryptionTime {
    param(
        [string]$Algorithm,
        [string]$InputFile,
        [string]$OutputFile,
        [string]$KeyFile,
        [string]$IVFile,
        [string]$PublicKeyFile,
        [int]$Iterations
    )
    
    $times = @()
    $successCount = 0
    
    for ($i = 1; $i -le $Iterations; $i++) {
        try {
            $time = Measure-Command {
                switch ($Algorithm) {
                    "DES" {
                        $key = (Get-Content $KeyFile -Raw).Trim()
                        $iv = (Get-Content $IVFile -Raw).Trim()
                        openssl enc -e -des-cbc -provider-path $ProviderPath -provider default -provider legacy -in $InputFile -out $OutputFile -K $key -iv $iv -nosalt 2>&1 | Out-Null
                    }
                    "DES-EDE" {
                        $key = (Get-Content $KeyFile -Raw).Trim()
                        $iv = (Get-Content $IVFile -Raw).Trim()
                        openssl enc -e -des-ede-cbc -provider-path $ProviderPath -provider default -provider legacy -in $InputFile -out $OutputFile -K $key -iv $iv -nosalt 2>&1 | Out-Null
                    }
                    "DES3" {
                        $key = (Get-Content $KeyFile -Raw).Trim()
                        $iv = (Get-Content $IVFile -Raw).Trim()
                        openssl enc -e -des3 -provider-path $ProviderPath -provider default -provider legacy -in $InputFile -out $OutputFile -K $key -iv $iv -nosalt 2>&1 | Out-Null
                    }
                    "RSA" {
                        openssl pkeyutl -encrypt -pubin -inkey $PublicKeyFile -in $InputFile -out $OutputFile 2>&1 | Out-Null
                    }
                }
            }
            
            if ($LASTEXITCODE -eq 0) {
                $times += $time.TotalMilliseconds
                $successCount++
            } else {
                Write-Host "  Итерация $i : Ошибка" -ForegroundColor Red
            }
        } catch {
            Write-Host "  Итерация $i : Исключение: $_" -ForegroundColor Red
        }
    }
    
    if ($times.Count -eq 0) {
        return @{
            Average = 0
            Min = 0
            Max = 0
            SuccessCount = 0
            AllTimes = @()
        }
    }
    
    return @{
        Average = ($times | Measure-Object -Average).Average
        Min = ($times | Measure-Object -Minimum).Minimum
        Max = ($times | Measure-Object -Maximum).Maximum
        SuccessCount = $successCount
        AllTimes = $times
    }
}

# Генерация ключей и IV
Write-Host "`nГенерация ключей и IV..." -ForegroundColor Yellow

# DES
$desKeyFile = Join-Path $workDir "des_key.txt"
$desIVFile = Join-Path $workDir "des_iv.txt"
openssl rand -hex 8 | Out-File -FilePath $desKeyFile -Encoding ASCII -NoNewline
openssl rand -hex 8 | Out-File -FilePath $desIVFile -Encoding ASCII -NoNewline
Write-Host "  DES: ключ и IV сгенерированы" -ForegroundColor Gray

# DES-EDE
$desEdeKeyFile = Join-Path $workDir "des_ede_key.txt"
$desEdeIVFile = Join-Path $workDir "des_ede_iv.txt"
openssl rand -hex 16 | Out-File -FilePath $desEdeKeyFile -Encoding ASCII -NoNewline
openssl rand -hex 8 | Out-File -FilePath $desEdeIVFile -Encoding ASCII -NoNewline
Write-Host "  DES-EDE: ключ и IV сгенерированы" -ForegroundColor Gray

# DES3
$des3KeyFile = Join-Path $workDir "des3_key.txt"
$des3IVFile = Join-Path $workDir "des3_iv.txt"
openssl rand -hex 24 | Out-File -FilePath $des3KeyFile -Encoding ASCII -NoNewline
openssl rand -hex 8 | Out-File -FilePath $des3IVFile -Encoding ASCII -NoNewline
Write-Host "  DES3: ключ и IV сгенерированы" -ForegroundColor Gray

# RSA
$rsaPrivateKeyFile = Join-Path $workDir "privateRSA.pem"
$rsaPublicKeyFile = Join-Path $workDir "publicRSA.pem"

if (-not (Test-Path $rsaPrivateKeyFile)) {
    Write-Host "  RSA: генерация пары ключей (это может занять некоторое время)..." -ForegroundColor Gray
    openssl genpkey -algorithm RSA -out $rsaPrivateKeyFile -provider-path $ProviderPath -provider default -provider legacy -pkeyopt rsa_keygen_bits:2048 2>&1 | Out-Null
    openssl rsa -in $rsaPrivateKeyFile -out $rsaPublicKeyFile -pubout 2>&1 | Out-Null
    Write-Host "  RSA: ключи сгенерированы" -ForegroundColor Gray
} else {
    Write-Host "  RSA: использование существующих ключей" -ForegroundColor Gray
    if (-not (Test-Path $rsaPublicKeyFile)) {
        openssl rsa -in $rsaPrivateKeyFile -out $rsaPublicKeyFile -pubout 2>&1 | Out-Null
    }
}

# Результаты
$results = @{}

# Измерение времени для каждого алгоритма
Write-Host "`n=== Измерение времени шифрования ===" -ForegroundColor Cyan

# DES
Write-Host "`nDES..." -ForegroundColor Yellow
$desOutputFile = Join-Path $workDir "plain_des.enc"
$desResult = Measure-EncryptionTime -Algorithm "DES" -InputFile $InputFile -OutputFile $desOutputFile -KeyFile $desKeyFile -IVFile $desIVFile -Iterations $Iterations
$results["DES"] = $desResult
Write-Host "  Среднее: $([math]::Round($desResult.Average, 2)) мс | Мин: $([math]::Round($desResult.Min, 2)) мс | Макс: $([math]::Round($desResult.Max, 2)) мс" -ForegroundColor Green

# DES-EDE
Write-Host "`nDES-EDE..." -ForegroundColor Yellow
$desEdeOutputFile = Join-Path $workDir "plain_des_ede.enc"
$desEdeResult = Measure-EncryptionTime -Algorithm "DES-EDE" -InputFile $InputFile -OutputFile $desEdeOutputFile -KeyFile $desEdeKeyFile -IVFile $desEdeIVFile -Iterations $Iterations
$results["DES-EDE"] = $desEdeResult
Write-Host "  Среднее: $([math]::Round($desEdeResult.Average, 2)) мс | Мин: $([math]::Round($desEdeResult.Min, 2)) мс | Макс: $([math]::Round($desEdeResult.Max, 2)) мс" -ForegroundColor Green

# DES3
Write-Host "`nDES3..." -ForegroundColor Yellow
$des3OutputFile = Join-Path $workDir "plain_des3.enc"
$des3Result = Measure-EncryptionTime -Algorithm "DES3" -InputFile $InputFile -OutputFile $des3OutputFile -KeyFile $des3KeyFile -IVFile $des3IVFile -Iterations $Iterations
$results["DES3"] = $des3Result
Write-Host "  Среднее: $([math]::Round($des3Result.Average, 2)) мс | Мин: $([math]::Round($des3Result.Min, 2)) мс | Макс: $([math]::Round($des3Result.Max, 2)) мс" -ForegroundColor Green

# RSA
Write-Host "`nRSA..." -ForegroundColor Yellow
$rsaOutputFile = Join-Path $workDir "plain_rsa.enc"
$rsaResult = Measure-EncryptionTime -Algorithm "RSA" -InputFile $InputFile -OutputFile $rsaOutputFile -PublicKeyFile $rsaPublicKeyFile -Iterations $Iterations
$results["RSA"] = $rsaResult
if ($rsaResult.SuccessCount -gt 0) {
    Write-Host "  Среднее: $([math]::Round($rsaResult.Average, 2)) мс | Мин: $([math]::Round($rsaResult.Min, 2)) мс | Макс: $([math]::Round($rsaResult.Max, 2)) мс" -ForegroundColor Green
} else {
    Write-Host "  Ошибка: не удалось выполнить шифрование RSA" -ForegroundColor Red
}

# Вывод сравнительной таблицы
Write-Host "`n=== Сравнительная таблица результатов ===" -ForegroundColor Cyan
Write-Host ""
Write-Host ("{0,-12} {1,-20} {2,-25} {3,-20} {4,-20}" -f "Алгоритм", "Размер ключа", "Среднее время (мс)", "Мин. время (мс)", "Макс. время (мс)")
Write-Host ("{0,-12} {1,-20} {2,-25} {3,-20} {4,-20}" -f ("-" * 12), ("-" * 20), ("-" * 25), ("-" * 20), ("-" * 20))

foreach ($algorithm in @("DES", "DES-EDE", "DES3", "RSA")) {
    if ($results.ContainsKey($algorithm) -and $results[$algorithm].SuccessCount -gt 0) {
        $keySize = switch ($algorithm) {
            "DES" { "64 бита (8 байт)" }
            "DES-EDE" { "128 бит (16 байт)" }
            "DES3" { "192 бита (24 байта)" }
            "RSA" { "2048 бит" }
        }
        $avg = [math]::Round($results[$algorithm].Average, 2)
        $min = [math]::Round($results[$algorithm].Min, 2)
        $max = [math]::Round($results[$algorithm].Max, 2)
        Write-Host ("{0,-12} {1,-20} {2,-25} {3,-20} {4,-20}" -f $algorithm, $keySize, $avg, $min, $max)
    } else {
        Write-Host ("{0,-12} {1,-20} {2,-25}" -f $algorithm, "N/A", "Ошибка") -ForegroundColor Red
    }
}

# Анализ результатов
Write-Host "`n=== Анализ результатов ===" -ForegroundColor Cyan

if ($results["DES"].SuccessCount -gt 0 -and $results["DES-EDE"].SuccessCount -gt 0) {
    $desEdeRatio = [math]::Round($results["DES-EDE"].Average / $results["DES"].Average, 2)
    Write-Host "DES-EDE медленнее DES в $desEdeRatio раз" -ForegroundColor Yellow
}

if ($results["DES"].SuccessCount -gt 0 -and $results["DES3"].SuccessCount -gt 0) {
    $des3Ratio = [math]::Round($results["DES3"].Average / $results["DES"].Average, 2)
    Write-Host "DES3 медленнее DES в $des3Ratio раз" -ForegroundColor Yellow
}

if ($results["DES"].SuccessCount -gt 0 -and $results["RSA"].SuccessCount -gt 0) {
    $rsaRatio = [math]::Round($results["RSA"].Average / $results["DES"].Average, 2)
    Write-Host "RSA медленнее DES в $rsaRatio раз" -ForegroundColor Yellow
}

# Определение самого быстрого алгоритма
$validResults = $results.GetEnumerator() | Where-Object { $_.Value.SuccessCount -gt 0 } | Sort-Object { $_.Value.Average }
if ($validResults.Count -gt 0) {
    $fastest = $validResults[0]
    Write-Host "`nСамый быстрый алгоритм: $($fastest.Key) ($([math]::Round($fastest.Value.Average, 2)) мс)" -ForegroundColor Green
}

# Сохранение результатов в файл
$resultsFile = Join-Path $workDir "encryption_comparison_results.txt"
$resultsContent = @"
=== Результаты сравнения времени шифрования ===
Дата: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Входной файл: $InputFile
Размер файла: $fileSize байт
Количество итераций: $Iterations

Сравнительная таблица:
"@

foreach ($algorithm in @("DES", "DES-EDE", "DES3", "RSA")) {
    if ($results.ContainsKey($algorithm) -and $results[$algorithm].SuccessCount -gt 0) {
        $keySize = switch ($algorithm) {
            "DES" { "64 бита (8 байт)" }
            "DES-EDE" { "128 бит (16 байт)" }
            "DES3" { "192 бита (24 байта)" }
            "RSA" { "2048 бит" }
        }
        $result = $results[$algorithm]
        $resultsContent += "`n${algorithm}:`n"
        $resultsContent += "  Размер ключа: $keySize`n"
        $resultsContent += "  Среднее время: $([math]::Round($result.Average, 2)) мс`n"
        $resultsContent += "  Минимальное время: $([math]::Round($result.Min, 2)) мс`n"
        $resultsContent += "  Максимальное время: $([math]::Round($result.Max, 2)) мс`n"
        $resultsContent += "  Успешных итераций: $($result.SuccessCount) из $Iterations`n"
        $resultsContent += "  Все значения: $($result.AllTimes -join ', ') мс`n"
    }
}

$resultsContent | Out-File -FilePath $resultsFile -Encoding UTF8
Write-Host "`nРезультаты сохранены в: $resultsFile" -ForegroundColor Green

Write-Host "`n=== Сравнение завершено ===" -ForegroundColor Cyan

