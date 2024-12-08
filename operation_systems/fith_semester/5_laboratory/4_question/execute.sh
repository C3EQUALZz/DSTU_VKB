#!/bin/bash

# Создаем файл для хранения информации
touch system_info.txt

# Добавляем информацию о системе
echo "System Information" > system_info.txt
uname -a >> system_info.txt
echo "" >> system_info.txt

# Добавляем информацию о дисках и их разметке
echo "Disk Information" >> system_info.txt
lsblk >> system_info.txt
echo "" >> system_info.txt

echo "Disk Partition Information" >> system_info.txt
sudo fdisk -l >> system_info.txt
echo "" >> system_info.txt

# Добавляем информацию о файловых системах
echo "Filesystem Information" >> system_info.txt
df -h >> system_info.txt
echo "" >> system_info.txt

# Добавляем информацию о загруженных модулях ядра
echo "Loaded Kernel Modules" >> system_info.txt
lsmod >> system_info.txt
echo "" >> system_info.txt

# Добавляем информацию о процессоре и памяти
echo "CPU Information" >> system_info.txt
lscpu >> system_info.txt
echo "" >> system_info.txt

echo "Memory Information" >> system_info.txt
free -h >> system_info.txt
echo "" >> system_info.txt
