# PowerShell скрипт для автоматизации шифрования DES-EDE и 3DES с измерением времени
# Использование: .\des3-automation.ps1 -InputFile "plain.txt" [-Password "password"] [-KeyFile "key.txt"]

param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,
    
    [Parameter(Mandatory=$false)]
    [string]$Password,
    
    [Parameter(Mandatory=$false)]
    [string]$KeyFile = "key.txt",
    
    [Parameter(Mandatory=$false)]
    [string]$IVFile = "iv.txt"
)

# Проверка наличия входного файла
if (-not (Test-Path $InputFile)) {
    Write-Host "Ошибка: Файл '$InputFile' не найден!" -ForegroundColor Red
    exit 1
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

# Имена выходных файлов
$encryptedFile = "enc.txt"
$decryptedFile = "newfile.txt"

Write-Host "`n=== Автоматизация шифрования DES-EDE и 3DES ===" -ForegroundColor Cyan
Write-Host "Входной файл: $InputFile" -ForegroundColor Yellow

# Генерация ключа и IV, если не указан пароль
if ([string]::IsNullOrEmpty($Password)) {
    Write-Host "`nГенерация ключа и IV..." -ForegroundColor Yellow
    $key = openssl rand -hex 24
    $iv = openssl rand -hex 8
    
    # Сохранение ключа и IV в файлы
    $key | Out-File -FilePath $KeyFile -Encoding ASCII -NoNewline
    $iv | Out-File -FilePath $IVFile -Encoding ASCII -NoNewline
    
    Write-Host "Ключ сохранен в: $KeyFile" -ForegroundColor Green
    Write-Host "IV сохранен в: $IVFile" -ForegroundColor Green
    
    $useKeyFile = $true
} else {
    $useKeyFile = $false
    Write-Host "Использование пароля для шифрования" -ForegroundColor Yellow
}

# Функция для шифрования с измерением времени
function Encrypt-File {
    param([string]$inputFile, [string]$outputFile, [string]$key, [string]$iv, [string]$pass, [bool]$useKey)
    
    $encryptCommand = "openssl enc -des3 -e -in `"$inputFile`" -out `"$outputFile`""
    
    if ($useKey) {
        $encryptCommand += " -K $key -iv $iv"
    }
    
    Write-Host "`nВыполнение шифрования..." -ForegroundColor Yellow
    Write-Host "Команда: $encryptCommand" -ForegroundColor Gray
    
    $encryptTime = Measure-Command {
        if ($useKey) {
            openssl enc -des3 -e -in $inputFile -out $outputFile -K $key -iv $iv 2>&1 | Out-Null
        } else {
            # Использование пароля через -pass pass:password
            openssl enc -des3 -e -in $inputFile -out $outputFile -pass pass:$pass 2>&1 | Out-Null
        }
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Шифрование завершено успешно!" -ForegroundColor Green
        Write-Host "Время шифрования: $($encryptTime.TotalMilliseconds) мс" -ForegroundColor Cyan
        return $encryptTime
    } else {
        Write-Host "Ошибка при шифровании!" -ForegroundColor Red
        return $null
    }
}

# Функция для расшифрования с измерением времени
function Decrypt-File {
    param([string]$inputFile, [string]$outputFile, [string]$key, [string]$iv, [string]$pass, [bool]$useKey)
    
    $decryptCommand = "openssl enc -des3 -d -in `"$inputFile`" -out `"$outputFile`""
    
    if ($useKey) {
        $decryptCommand += " -K $key -iv $iv"
    }
    
    Write-Host "`nВыполнение расшифрования..." -ForegroundColor Yellow
    Write-Host "Команда: $decryptCommand" -ForegroundColor Gray
    
    $decryptTime = Measure-Command {
        if ($useKey) {
            openssl enc -des3 -d -in $inputFile -out $outputFile -K $key -iv $iv 2>&1 | Out-Null
        } else {
            # Использование пароля через -pass pass:password
            openssl enc -des3 -d -in $inputFile -out $outputFile -pass pass:$pass 2>&1 | Out-Null
        }
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Расшифрование завершено успешно!" -ForegroundColor Green
        Write-Host "Время расшифрования: $($decryptTime.TotalMilliseconds) мс" -ForegroundColor Cyan
        return $decryptTime
    } else {
        Write-Host "Ошибка при расшифровании!" -ForegroundColor Red
        return $null
    }
}

# Функция для сравнения файлов
function Compare-Files {
    param([string]$file1, [string]$file2)
    
    if (-not (Test-Path $file1) -or -not (Test-Path $file2)) {
        Write-Host "Ошибка: Один из файлов для сравнения не найден!" -ForegroundColor Red
        return $false
    }
    
    $hash1 = (Get-FileHash $file1 -Algorithm SHA256).Hash
    $hash2 = (Get-FileHash $file2 -Algorithm SHA256).Hash
    
    if ($hash1 -eq $hash2) {
        Write-Host "`n✓ Файлы идентичны! SHA256 хеши совпадают." -ForegroundColor Green
        return $true
    } else {
        Write-Host "`n✗ Файлы различаются!" -ForegroundColor Red
        Write-Host "Хеш исходного файла: $hash1" -ForegroundColor Yellow
        Write-Host "Хеш расшифрованного файла: $hash2" -ForegroundColor Yellow
        return $false
    }
}

# Основной процесс
try {
    # Шифрование
    if ($useKeyFile) {
        $keyContent = (Get-Content $KeyFile -Raw).Trim()
        $ivContent = (Get-Content $IVFile -Raw).Trim()
        $encryptTime = Encrypt-File -inputFile $InputFile -outputFile $encryptedFile -key $keyContent -iv $ivContent -pass $null -useKey $true
    } else {
        $encryptTime = Encrypt-File -inputFile $InputFile -outputFile $encryptedFile -key $null -iv $null -pass $Password -useKey $false
    }
    
    if ($null -eq $encryptTime) {
        exit 1
    }
    
    # Расшифрование
    if ($useKeyFile) {
        $keyContent = (Get-Content $KeyFile -Raw).Trim()
        $ivContent = (Get-Content $IVFile -Raw).Trim()
        $decryptTime = Decrypt-File -inputFile $encryptedFile -outputFile $decryptedFile -key $keyContent -iv $ivContent -pass $null -useKey $true
    } else {
        $decryptTime = Decrypt-File -inputFile $encryptedFile -outputFile $decryptedFile -key $null -iv $null -pass $Password -useKey $false
    }
    
    if ($null -eq $decryptTime) {
        exit 1
    }
    
    # Сравнение файлов
    $filesMatch = Compare-Files -file1 $InputFile -file2 $decryptedFile
    
    # Вывод итоговой статистики
    Write-Host "`n=== Итоговая статистика ===" -ForegroundColor Cyan
    Write-Host "Время шифрования: $($encryptTime.TotalMilliseconds) мс ($($encryptTime.TotalSeconds) сек)" -ForegroundColor Yellow
    Write-Host "Время расшифрования: $($decryptTime.TotalMilliseconds) мс ($($decryptTime.TotalSeconds) сек)" -ForegroundColor Yellow
    Write-Host "Общее время: $($($encryptTime + $decryptTime).TotalMilliseconds) мс ($($($encryptTime + $decryptTime).TotalSeconds) сек)" -ForegroundColor Yellow
    
    # Размеры файлов
    $inputSize = (Get-Item $InputFile).Length
    $encryptedSize = (Get-Item $encryptedFile).Length
    Write-Host "`nРазмер исходного файла: $inputSize байт" -ForegroundColor Gray
    Write-Host "Размер зашифрованного файла: $encryptedSize байт" -ForegroundColor Gray
    
    if ($filesMatch) {
        Write-Host "`n✓ Все операции выполнены успешно!" -ForegroundColor Green
    } else {
        Write-Host "`n⚠ Внимание: Файлы не совпадают!" -ForegroundColor Red
    }
    
} catch {
    Write-Host "`nОшибка при выполнении скрипта: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`nСкрипт завершен." -ForegroundColor Cyan
