Add-Type -AssemblyName PresentationFramework
$Message = "Скрипт выполнен успешно!"
$Title = "Уведомление"
[System.Windows.MessageBox]::Show($Message, $Title, [System.Windows.MessageBoxButton]::OK, [System.Windows.MessageBoxImage]::Information)