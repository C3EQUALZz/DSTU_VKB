#Requires -Version 5.1
<#
.SYNOPSIS
    Сводный отчёт по инвентаризации состава технических средств ПК (табл. 2 ЛР 2).

.DESCRIPTION
    Скрипт заменяет ручной обход "Диспетчера устройств". Для каждой категории
    устройств (класса Диспетчера) он получает по каждому экземпляру:
        - Тип устройства (наименование ТС) — понятное имя устройства;
        - Номер версии драйвера        — DEVPKEY_Device_DriverVersion;
        - Производитель                — DEVPKEY_Device_Manufacturer;
        - Размещение                   — DEVPKEY_Device_LocationInfo.

    Категории соответствуют строкам таблицы 2. Если в системе нет устройств
    данной категории (например «Модемы», «Разъёмы памяти»), строка выводится
    с прочерками «-», как в образце.

.PARAMETER HtmlPath
    Путь для выгрузки результата в HTML-файл с готовой таблицей (4 колонки,
    объединённая ячейка категории через rowspan — как в образце). По умолчанию
    рядом со скриптом создаётся «Таблица2.html». Открой файл в браузере,
    выдели всё (Ctrl+A), скопируй (Ctrl+C) и вставь в Word (Ctrl+V) — получится
    настоящая таблица.

.PARAMETER NoOpen
    Не открывать HTML-файл в браузере автоматически.

.PARAMETER CsvPath
    Дополнительная выгрузка в CSV (UTF-8, разделитель «;») для Excel.

.PARAMETER IncludeHidden
    Показывать также отключённые/скрытые (не подключённые сейчас) устройства.

.EXAMPLE
    .\Get-HardwareInventory.ps1
    Вывод в консоль + HTML-файл Таблица2.html открывается в браузере.

.EXAMPLE
    .\Get-HardwareInventory.ps1 -CsvPath .\Инвентаризация.csv
    То же + дополнительная выгрузка в CSV.

.NOTES
    Запуск: PowerShell (обычных прав достаточно; часть свойств полнее
    под администратором). При ошибке политики выполнения запускать так:
        powershell -ExecutionPolicy Bypass -File .\Get-HardwareInventory.ps1
#>

[CmdletBinding()]
param(
    [string] $HtmlPath,
    [switch] $NoOpen,
    [string] $CsvPath,
    [switch] $IncludeHidden
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Путь к HTML по умолчанию — рядом со скриптом. $PSScriptRoot недоступен
# в блоке param, поэтому вычисляем здесь. Запасной вариант — текущая папка.
if (-not $HtmlPath) {
    $baseDir = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
    $HtmlPath = Join-Path $baseDir 'Таблица2.html'
}

# --- Ключи свойств Windows PnP (DEVPKEY) ---------------------------------
$PKEY_DriverVersion = 'DEVPKEY_Device_DriverVersion'
$PKEY_Manufacturer  = 'DEVPKEY_Device_Manufacturer'
$PKEY_LocationInfo  = 'DEVPKEY_Device_LocationInfo'
$PLACEHOLDER        = '-'

# --- Соответствие строк таблицы 2 классам "Диспетчера устройств" ----------
# Наименование строки таблицы  ->  один или несколько PnP-классов Windows.
$Categories = [ordered]@{
    'Дисковые устройства'                     = @('DiskDrive')
    'Процессор (процессоры)'                  = @('Processor')
    'Звуковые, видео и игровые устройства'    = @('MEDIA')
    # Материнская плата в Диспетчере отдельным классом не представлена —
    # в образце тут прочерк, поэтому классов не назначаем (строка = «-»).
    'Материнская плата'                       = @()
    'DVD и CD-ROM дисководы'                   = @('CDROM')
    'Контроллеры USB'                         = @('USB')
    'Монитор'                                 = @('Monitor')
    'Видеоадаптер(ы)'                         = @('Display')
    'Сетевые адаптеры'                        = @('Net')
    'Модемы'                                  = @('Modem')
    'Разъёмы памяти'                          = @('MemoryTechnologyDevice', 'SCMDisk')
    'IDE ATA/ATAPI контроллеры'               = @('hdc')
    'Клавиатуры'                              = @('Keyboard')
    'Устройства HID'                          = @('HIDClass')
}

# --- Получение одного свойства устройства с защитой от пустых значений -----
function Get-DeviceProp {
    param(
        [Parameter(Mandatory)] $Device,
        [Parameter(Mandatory)] [string] $KeyName
    )
    try {
        $prop = Get-PnpDeviceProperty -InstanceId $Device.InstanceId -KeyName $KeyName -ErrorAction Stop
        $value = $prop.Data
        if ($null -ne $value -and "$value".Trim().Length -gt 0) {
            return "$value".Trim()
        }
    }
    catch {
        # свойство недоступно для этого устройства — вернём прочерк
    }
    return $PLACEHOLDER
}

# --- Сбор данных ----------------------------------------------------------
# $groups — упорядоченный список строк таблицы. Каждый элемент:
#   Category — наименование ТС (строка таблицы 2);
#   Rows     — массив устройств: @{ Version; Manufacturer; Location }.
# Пустая категория содержит одну строку с прочерками.
$groups = New-Object System.Collections.Generic.List[object]

foreach ($category in $Categories.Keys) {
    $classes = $Categories[$category]

    # Собираем устройства всех классов, отнесённых к строке таблицы.
    $devices = @()
    foreach ($class in $classes) {
        try {
            $found = Get-PnpDevice -Class $class -ErrorAction Stop
            if (-not $IncludeHidden) {
                # только реально присутствующие устройства
                $found = $found | Where-Object { $_.Present }
            }
            if ($found) { $devices += $found }
        }
        catch {
            # класс отсутствует в системе — пропускаем
        }
    }

    # @(...) гарантирует массив: Sort-Object с одним элементом иначе вернёт
    # скаляр, и обращение к .Count падает под Set-StrictMode.
    $devices = @($devices | Sort-Object -Property FriendlyName -Unique)

    $rows = New-Object System.Collections.Generic.List[object]
    if ($devices.Count -eq 0) {
        # Категория пустая (как «Модемы», «Разъёмы памяти» в образце) — прочерки.
        $rows.Add([pscustomobject]@{
            Version      = $PLACEHOLDER
            Manufacturer = $PLACEHOLDER
            Location     = $PLACEHOLDER
        })
    }
    else {
        foreach ($dev in $devices) {
            $rows.Add([pscustomobject]@{
                Version      = Get-DeviceProp -Device $dev -KeyName $PKEY_DriverVersion
                Manufacturer = Get-DeviceProp -Device $dev -KeyName $PKEY_Manufacturer
                Location     = Get-DeviceProp -Device $dev -KeyName $PKEY_LocationInfo
            })
        }
    }

    $groups.Add([pscustomobject]@{
        Category = $category
        Rows     = $rows
    })
}

# --- Плоское представление для консоли и CSV ------------------------------
$report = New-Object System.Collections.Generic.List[object]
foreach ($g in $groups) {
    $first = $true
    foreach ($r in $g.Rows) {
        $report.Add([pscustomobject]@{
            'Тип устройства'  = if ($first) { $g.Category } else { '' }
            'Версия драйвера' = $r.Version
            'Производитель'   = $r.Manufacturer
            'Размещение'      = $r.Location
        })
        $first = $false
    }
}

# --- Вывод в консоль ------------------------------------------------------
Write-Host ''
Write-Host 'Таблица 2 — Сводный отчёт по инвентаризации состава ТС ПК' -ForegroundColor Cyan
Write-Host ''

$report |
    Format-Table -AutoSize -Wrap `
        -Property 'Тип устройства', 'Версия драйвера', 'Производитель', 'Размещение'

# --- Генерация HTML-таблицы (для вставки в Word) --------------------------
# Категория выводится одной объединённой ячейкой (rowspan) на все свои строки —
# как «Контроллеры USB» в образце.
# Экранируем спецсимволы HTML. -replace работает с regex; '&' в шаблоне
# литерален, поэтому заменяем его первым.
function Encode-Html {
    param($Text)
    $s = [string]$Text
    $s = $s -replace '&', '&amp;'
    $s = $s -replace '<', '&lt;'
    $s = $s -replace '>', '&gt;'
    return $s
}

try {
    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add('<!DOCTYPE html>')
    $lines.Add('<html lang="ru"><head><meta charset="utf-8">')
    $lines.Add('<title>Таблица 2 — Сводный отчёт по инвентаризации состава ТС ПК</title>')
    $lines.Add('<style>')
    $lines.Add('  body{font-family:"Times New Roman",serif;font-size:14px;padding:16px;}')
    $lines.Add('  caption{font-weight:bold;text-align:center;margin-bottom:8px;font-size:15px;}')
    $lines.Add('  table{border-collapse:collapse;width:100%;}')
    $lines.Add('  th,td{border:1px solid #000;padding:4px 8px;vertical-align:top;text-align:left;}')
    $lines.Add('  th{font-weight:bold;text-align:center;}')
    $lines.Add('</style></head><body>')
    $lines.Add('<table>')
    $lines.Add('<caption>Таблица 2 — Сводный отчёт по инвентаризации состава ТС ПК</caption>')
    $lines.Add('<thead><tr>')
    $lines.Add('  <th>Тип устройства (наименование ТС)</th>')
    $lines.Add('  <th>Номер версии драйвера</th>')
    $lines.Add('  <th>Производитель</th>')
    $lines.Add('  <th>Размещение</th>')
    $lines.Add('</tr></thead><tbody>')

    foreach ($g in $groups) {
        # $g.Rows — уже List[object]; работаем напрямую через .Count и [$i]
        # (обёртка @() вокруг List вызывала ArgumentException).
        $rowsList = $g.Rows
        $span     = $rowsList.Count
        for ($i = 0; $i -lt $span; $i++) {
            $r = $rowsList[$i]
            $lines.Add('<tr>')
            if ($i -eq 0) {
                # Ячейка категории объединяется на все строки устройств (rowspan).
                $cat = Encode-Html $g.Category
                $lines.Add('  <td rowspan="' + $span + '">' + $cat + '</td>')
            }
            $lines.Add('  <td>' + (Encode-Html $r.Version) + '</td>')
            $lines.Add('  <td>' + (Encode-Html $r.Manufacturer) + '</td>')
            $lines.Add('  <td>' + (Encode-Html $r.Location) + '</td>')
            $lines.Add('</tr>')
        }
    }

    $lines.Add('</tbody></table></body></html>')

    # Out-File -Encoding utf8 в Windows PowerShell 5.1 пишет UTF-8 с BOM —
    # браузер и Word гарантированно распознают кириллицу.
    ($lines -join [Environment]::NewLine) | Out-File -FilePath $HtmlPath -Encoding utf8

    Write-Host ''
    Write-Host "HTML-таблица сохранена: $HtmlPath" -ForegroundColor Green
    Write-Host 'Открой файл, выдели всё (Ctrl+A), скопируй (Ctrl+C) и вставь в Word (Ctrl+V).' -ForegroundColor Green

    if (-not $NoOpen) {
        Start-Process $HtmlPath
    }
}
catch {
    Write-Host ''
    Write-Host 'ОШИБКА при генерации/открытии HTML:' -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host $_.InvocationInfo.PositionMessage -ForegroundColor Red
    if (Test-Path $HtmlPath) {
        Write-Host "Файл всё же создан, открой вручную: $HtmlPath" -ForegroundColor Yellow
    }
}

# --- Экспорт в CSV (опционально) ------------------------------------------
if ($CsvPath) {
    $exportCols = 'Тип устройства', 'Версия драйвера', 'Производитель', 'Размещение'
    $report |
        Select-Object -Property $exportCols |
        Export-Csv -Path $CsvPath -NoTypeInformation -Encoding UTF8 -Delimiter ';'
    Write-Host ''
    Write-Host "CSV сохранён: $CsvPath" -ForegroundColor Green
}
