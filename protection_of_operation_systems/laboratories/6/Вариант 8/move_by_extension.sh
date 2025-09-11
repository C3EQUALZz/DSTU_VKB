#!/bin/bash

echo "Перемещение файлов по расширениям из текущей папки"
echo "=================================================="

texts_dir="texts"
images_dir="images"

# Создаем папки, если их нет
mkdir -p "$texts_dir" "$images_dir"

moved_txt=0
moved_images=0

declare -a moved_txt_files
declare -a moved_image_files

# Собираем списки файлов только из текущей директории
mapfile -d '' txt_files < <(find . -maxdepth 1 -type f -name "*.txt" -print0)
mapfile -d '' bmp_files < <(find . -maxdepth 1 -type f -name "*.bmp" -print0)
mapfile -d '' jpg_files < <(find . -maxdepth 1 -type f -name "*.jpg" -print0)

# Перемещение txt → texts
if [ ${#txt_files[@]} -gt 0 ]; then
	echo "Перемещаю .txt файлы в $texts_dir ..."
	for f in "${txt_files[@]}"; do
		src="${f#./}"
		if mv -- "$src" "$texts_dir/" 2>/dev/null; then
			moved_txt_files+=("$src → $texts_dir/")
			((moved_txt++))
		else
			echo "Ошибка при перемещении: $src"
		fi
	done
else
	echo "Файлы .txt в текущей папке не найдены."
fi

# Объединяем bmp и jpg
image_files=("${bmp_files[@]}" "${jpg_files[@]}")

# Перемещение bmp/jpg → images
if [ ${#image_files[@]} -gt 0 ]; then
	echo "Перемещаю .bmp и .jpg файлы в $images_dir ..."
	for f in "${image_files[@]}"; do
		src="${f#./}"
		if mv -- "$src" "$images_dir/" 2>/dev/null; then
			moved_image_files+=("$src → $images_dir/")
			((moved_images++))
		else
			echo "Ошибка при перемещении: $src"
		fi
	done
else
	echo "Файлы .bmp/.jpg в текущей папке не найдены."
fi

echo ""
echo "=========================================="
echo "ИТОГИ ПЕРЕМЕЩЕНИЯ:"
echo "=========================================="

if [ $moved_txt -gt 0 ]; then
	echo "Перемещено .txt: $moved_txt"
	for item in "${moved_txt_files[@]}"; do
		printf "%s\n" "$item"
	done
else
	echo ".txt: нет перемещенных файлов"
fi

if [ $moved_images -gt 0 ]; then
	echo "Перемещено изображений (.bmp/.jpg): $moved_images"
	for item in "${moved_image_files[@]}"; do
		printf "%s\n" "$item"
	done
else
	echo ".bmp/.jpg: нет перемещенных файлов"
fi

echo ""
echo "Операция завершена!"
