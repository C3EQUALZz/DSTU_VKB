# Подключение сборки System.Windows.Forms
Add-Type -AssemblyName System.Windows.Forms

# Отображение всплывающего сообщения
[System.Windows.Forms.MessageBox]::Show("Hello, World!", "Message", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
