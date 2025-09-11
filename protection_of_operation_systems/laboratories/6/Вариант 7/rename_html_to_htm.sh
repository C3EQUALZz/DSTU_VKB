#!/bin/bash

echo "Переименование файлов .html → .htm в текущей папке"
echo "=================================================="

renamed_count=0

declare -a renamed_files

# Находим файлы только в текущей директории (без подпапок)
mapfile -d '' files < <(find . -maxdepth 1 -type f -name "*.html" -print0)

if [ ${#files[@]} -eq 0 ]; then
	echo "Файлы с расширением .html не найдены в текущей директории."
	exit 0
fi

echo "Найдено ${#files[@]} файлов с расширением .html"

echo "Начинаю переименование..."
for file in "${files[@]}"; do
	# Убираем префикс ./
	src="${file#./}"
	base_name="${src%.html}"
	dst="$base_name.htm"
	
	if [ -e "$dst" ]; then
		echo "Пропущено (уже существует): $src → $dst"
		continue
	fi
	
	if mv -- "$src" "$dst" 2>/dev/null; then
		echo "Переименовано: $src → $dst"
		renamed_files+=("$src → $dst")
		((renamed_count++))
	else
		echo "Ошибка при переименовании: $src"
	fi
done

echo ""
echo "=========================================="
echo "РЕЗУЛЬТАТЫ ПЕРЕИМЕНОВАНИЯ:"
echo "=========================================="

if [ $renamed_count -gt 0 ]; then
	printf "%s\n" "Список переименованных файлов:" 
	for item in "${renamed_files[@]}"; do
		printf "%s\n" "$item"
	done
else
	echo "Переименованных файлов нет."
fi

echo "Общее количество переименованных файлов: $renamed_count"

echo "Операция завершена!"
