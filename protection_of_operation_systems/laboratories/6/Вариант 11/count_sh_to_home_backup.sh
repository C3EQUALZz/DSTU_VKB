#!/bin/bash

echo "Подсчет количества .sh файлов в указанной папке"
echo "==============================================="

read -p "Введите путь к папке: " target_dir

# Удаляем пробелы по краям
trimmed_dir="$(echo -e "$target_dir" | sed -e 's/^\s\+//' -e 's/\s\+$//')"

if [ -z "$trimmed_dir" ]; then
	echo "Ошибка: путь не может быть пустым"
	exit 1
fi

if [ ! -d "$trimmed_dir" ]; then
	echo "Ошибка: папка не найдена: $trimmed_dir"
	exit 1
fi

# Папка и файл для вывода
backup_dir="$HOME/backups"
output_file="$backup_dir/sh.txt"

# Создаем папку backups в домашней директории, если ее нет
mkdir -p "$backup_dir"

# Считаем только файлы в указанной директории, без подпапок
count=$(find "$trimmed_dir" -maxdepth 1 -type f -name "*.sh" | wc -l | tr -d ' ')

# Записываем информацию в файл (перезаписываем)
echo "Каталог: $trimmed_dir" > "$output_file"
echo "Количество файлов с расширением .sh: $count" >> "$output_file"
echo "Дата: $(date)" >> "$output_file"

if [ $? -eq 0 ]; then
	echo "Готово. Результат записан в: $output_file"
else
	echo "Ошибка при записи файла: $output_file"
	exit 1
fi
