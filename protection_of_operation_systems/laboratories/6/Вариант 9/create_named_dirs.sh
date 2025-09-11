#!/bin/bash

echo "Создание 10 папок с заданным именем и порядковым номером"
echo "========================================================="

read -p "Введите базовое имя папок (например: group, lab, task): " base

# Удаляем ведущие/замыкающие пробелы
base_trimmed="$(echo -e "$base" | sed -e 's/^\s\+//' -e 's/\s\+$//')"

if [ -z "$base_trimmed" ]; then
	echo "Ошибка: имя не может быть пустым"
	exit 1
fi

created=0

echo "Начинаю создание папок: ${base_trimmed}1 .. ${base_trimmed}10"
for n in {1..10}; do
	name="${base_trimmed}$n"
	if mkdir -p -- "$name" 2>/dev/null; then
		echo "Создана папка: $name"
		((created++))
	else
		echo "Ошибка при создании: $name"
	fi
done

echo ""
echo "=========================================="
echo "ИТОГИ:"
echo "=========================================="
echo "Создано папок: $created из 10"

echo "Операция завершена!"
