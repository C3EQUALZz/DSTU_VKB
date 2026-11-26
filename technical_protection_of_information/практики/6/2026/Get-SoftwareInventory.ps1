#Requires -Version 5.1
<#
.SYNOPSIS
    Сводный отчёт по инвентаризации состава ПО АРМ (табл. 2 ЛР 2).

.DESCRIPTION
    Скрипт заменяет ручной просмотр компонента Windows «Программы и компоненты»
    (Панель управления → Программы → Программы и компоненты). Он читает те же
    источники, что и этот компонент, — ветки реестра деинсталляции:
        HKLM\...\Uninstall            (64-битные программы)
        HKLM\WOW6432Node\...\Uninstall (32-битные программы)
        HKCU\...\Uninstall            (программы текущего пользователя)

    Для каждой программы выводится:
        - Название ПО        — DisplayName;
        - Номер версии       — DisplayVersion (если нет — прочерк «–»);
        - Издатель           — Publisher;
        - Всего установлено  — число одинаковых записей (обычно 1).

    Отфильтровываются системные компоненты (SystemComponent = 1) и дочерние
    записи обновлений (ParentKeyName) — ровно как их скрывает «Программы и
    компоненты». Порядок — по алфавиту (как столбец «Имя» в компоненте).

.PARAMETER HtmlPath
    Путь для выгрузки в HTML-файл с готовой таблицей (4 колонки). По умолчанию
    рядом со скриптом создаётся «Таблица_ПО.html». Открой файл в браузере,
    выдели всё (Ctrl+A), скопируй (Ctrl+C) и вставь в Word (Ctrl+V) — получится
    настоящая таблица.

.PARAMETER NoOpen
    Не открывать HTML-файл в браузере автоматически.

.PARAMETER CsvPath
    Дополнительная выгрузка в CSV (UTF-8, разделитель «;») для Excel.

.EXAMPLE
    .\Get-SoftwareInventory.ps1
    Вывод в консоль + HTML-файл Таблица_ПО.html открывается в браузере.

.EXAMPLE
    .\Get-SoftwareInventory.ps1 -CsvPath .\ПО.csv
    То же + дополнительная выгрузка в CSV.

.NOTES
    Запуск обычных прав достаточно (ветка HKCU видна только текущему юзеру;
    под администратором список полнее). При ошибке политики выполнения:
        powershell -ExecutionPolicy Bypass -File .\Get-SoftwareInventory.ps1
#>

[CmdletBinding()]
param(
    [string] $HtmlPath,
    [switch] $NoOpen,
    [string] $CsvPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Путь к HTML по умолчанию — рядом со скриптом. $PSScriptRoot недоступен
# в блоке param, поэтому вычисляем здесь. Запасной вариант — текущая папка.
if (-not $HtmlPath) {
    $baseDir = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
    $HtmlPath = Join-Path $baseDir 'Таблица_ПО.html'
}

$PLACEHOLDER = '–'   # прочерк (en-dash) — как в образце для пустой версии

# --- Ветки реестра деинсталляции (источник «Программ и компонентов») --------
$UninstallPaths = @(
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
    'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*'
    'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
)

# --- Безопасное чтение свойства (реестровые записи неоднородны) -------------
# Под Set-StrictMode обращение к несуществующему свойству бросает ошибку,
# поэтому читаем через PSObject.Properties.
function Get-Prop {
    param($Object, [string] $Name)
    $p = $Object.PSObject.Properties[$Name]
    if ($p) { return $p.Value }
    return $null
}

# --- Сбор сырых записей ----------------------------------------------------
$raw = New-Object System.Collections.Generic.List[object]
foreach ($path in $UninstallPaths) {
    try {
        $items = Get-ItemProperty -Path $path -ErrorAction SilentlyContinue
        foreach ($item in $items) { $raw.Add($item) }
    }
    catch {
        # ветка отсутствует — пропускаем
    }
}

# --- Фильтр: как в «Программах и компонентах» ------------------------------
# Оставляем записи с именем; убираем системные компоненты и дочерние
# записи обновлений (у них задан ParentKeyName) — их компонент не показывает.
$apps = New-Object System.Collections.Generic.List[object]
foreach ($item in $raw) {
    $name = Get-Prop $item 'DisplayName'
    if (-not $name -or "$name".Trim().Length -eq 0) { continue }

    $systemComponent = Get-Prop $item 'SystemComponent'
    if ($systemComponent -eq 1) { continue }

    $parentKey = Get-Prop $item 'ParentKeyName'
    if ($parentKey) { continue }

    $version   = Get-Prop $item 'DisplayVersion'
    $publisher = Get-Prop $item 'Publisher'

    $apps.Add([pscustomobject]@{
        Name      = "$name".Trim()
        Version   = if ($version   -and "$version".Trim())   { "$version".Trim() }   else { $PLACEHOLDER }
        Publisher = if ($publisher -and "$publisher".Trim()) { "$publisher".Trim() } else { $PLACEHOLDER }
    })
}

# --- Группировка: «Всего установлено» = число одинаковых записей ------------
# Одинаковыми считаем записи с совпадающими названием, версией и издателем
# (две разные версии одной программы — как «Kaspersky» в образце — остаются
# отдельными строками).
$report = New-Object System.Collections.Generic.List[object]
$grouped = $apps |
    Group-Object -Property Name, Version, Publisher |
    Sort-Object -Property { $_.Group[0].Name }

foreach ($grp in $grouped) {
    $first = $grp.Group[0]
    $report.Add([pscustomobject]@{
        'Название ПО'      = $first.Name
        'Номер версии'     = $first.Version
        'Издатель'         = $first.Publisher
        'Всего установлено' = $grp.Count
    })
}

# --- Вывод в консоль ------------------------------------------------------
Write-Host ''
Write-Host 'Таблица 2 — Сводный отчёт по инвентаризации состава ПО АРМ' -ForegroundColor Cyan
Write-Host ("Всего программ: {0}" -f $report.Count) -ForegroundColor Cyan
Write-Host ''

$report |
    Format-Table -AutoSize -Wrap `
        -Property 'Название ПО', 'Номер версии', 'Издатель', 'Всего установлено'

# --- Генерация HTML-таблицы (для вставки в Word) --------------------------
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
    $lines.Add('<title>Таблица 2 — Сводный отчёт по инвентаризации состава ПО АРМ</title>')
    $lines.Add('<style>')
    $lines.Add('  body{font-family:"Times New Roman",serif;font-size:14px;padding:16px;}')
    $lines.Add('  caption{font-weight:bold;text-align:center;margin-bottom:8px;font-size:15px;}')
    $lines.Add('  table{border-collapse:collapse;width:100%;}')
    $lines.Add('  th,td{border:1px solid #000;padding:4px 8px;vertical-align:top;text-align:left;}')
    $lines.Add('  th{font-weight:bold;text-align:center;}')
    $lines.Add('  td.num{text-align:center;}')
    $lines.Add('</style></head><body>')
    $lines.Add('<table>')
    $lines.Add('<caption>Таблица 2 — Сводный отчёт по инвентаризации состава ПО АРМ</caption>')
    $lines.Add('<thead><tr>')
    $lines.Add('  <th>Название ПО</th>')
    $lines.Add('  <th>Номер версии</th>')
    $lines.Add('  <th>Издатель</th>')
    $lines.Add('  <th>Всего установлено</th>')
    $lines.Add('</tr></thead><tbody>')

    foreach ($row in $report) {
        $lines.Add('<tr>')
        $lines.Add('  <td>' + (Encode-Html $row.'Название ПО')  + '</td>')
        $lines.Add('  <td>' + (Encode-Html $row.'Номер версии') + '</td>')
        $lines.Add('  <td>' + (Encode-Html $row.'Издатель')     + '</td>')
        $lines.Add('  <td class="num">' + (Encode-Html $row.'Всего установлено') + '</td>')
        $lines.Add('</tr>')
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
    $exportCols = 'Название ПО', 'Номер версии', 'Издатель', 'Всего установлено'
    $report |
        Select-Object -Property $exportCols |
        Export-Csv -Path $CsvPath -NoTypeInformation -Encoding UTF8 -Delimiter ';'
    Write-Host ''
    Write-Host "CSV сохранён: $CsvPath" -ForegroundColor Green
}
