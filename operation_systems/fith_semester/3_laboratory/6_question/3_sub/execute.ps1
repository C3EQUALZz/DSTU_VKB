# Получаем информацию о логических дисках
$disks = Get-WmiObject Win32_LogicalDisk -Filter "DriveType=3"

# Выводим информацию о каждом диске
foreach ($disk in $disks) {
    $freeSpaceGB = [math]::round($disk.FreeSpace / 1GB, 2)
    $totalSpaceGB = [math]::round($disk.Size / 1GB, 2)
    $usedSpaceGB = [math]::round(($disk.Size - $disk.FreeSpace) / 1GB, 2)

    Write-Output "Диск: $($disk.DeviceID)"
    Write-Output "  Всего места: $totalSpaceGB GB"
    Write-Output "  Свободного места: $freeSpaceGB GB"
    Write-Output "  Занято места: $usedSpaceGB GB"
    Write-Output ""
}