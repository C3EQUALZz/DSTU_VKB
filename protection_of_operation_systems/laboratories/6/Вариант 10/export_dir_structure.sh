#!/bin/bash

echo "Экспорт структуры каталогов в файл"
echo "=================================="

read -p "Введите путь к папке: " target_dir

# Удаляем ведущие/замыкающие пробелы
trimmed_dir="$(echo -e "$target_dir" | sed -e 's/^\s\+//' -e 's/\s\+$//')"

if [ -z "$trimmed_dir" ]; then
	echo "Ошибка: путь не может быть пустым"
	exit 1
fi

if [ ! -d "$trimmed_dir" ]; then
	echo "Ошибка: папка не найдена: $trimmed_dir"
	exit 1
fi

# Формируем имя файла с текущей датой (в текущей директории)
date_str="$(date +%Y-%m-%d)"
output_file="dir_structure_${date_str}.txt"

{
	echo "Структура каталогов для: $trimmed_dir"
	echo "Дата: $(date)"
	echo "=================================="

	# Если есть tree — используем его (только каталоги)
	if command -v tree >/dev/null 2>&1; then
		tree -d "$trimmed_dir"
	else
		# Запасной вариант: find все каталоги и форматирование
		echo "(Примечание: утилита 'tree' не найдена, используется find)"
		# Печатаем корень и все вложенные каталоги
		printf "%s\n" "$trimmed_dir"
		find "$trimmed_dir" -type d -mindepth 1 | sed "s|^$trimmed_dir/||" | awk -F'/' '{
			indent="";
			for(i=1;i<NF;i++){indent=indent"  "}
			print indent $NF
		}'
	fi
} > "$output_file"

if [ $? -eq 0 ]; then
	echo "Готово. Структура записана в файл: $output_file"
else
	echo "Ошибка при записи файла: $output_file"
	exit 1
fi
