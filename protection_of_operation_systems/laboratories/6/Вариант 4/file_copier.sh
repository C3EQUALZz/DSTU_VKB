#!/bin/bash

echo "Программа для перемещения файлов с указанным расширением"
echo "======================================================"

# Запрашиваем расширение файлов у пользователя
read -p "Введите расширение файлов (без точки, например: doc, txt, pdf): " file_extension

# Проверяем, что расширение не пустое
if [ -z "$file_extension" ]; then
    echo "Ошибка: расширение не может быть пустым"
    exit 1
fi

# Запрашиваем папку назначения
read -p "Введите путь к папке назначения: " destination_dir

# Проверяем, что папка назначения не пустая
if [ -z "$destination_dir" ]; then
    echo "Ошибка: путь к папке назначения не может быть пустым"
    exit 1
fi

# Создаем папку назначения, если она не существует
if [ ! -d "$destination_dir" ]; then
    echo "Создаю папку назначения: $destination_dir"
    mkdir -p "$destination_dir"
    
    if [ $? -ne 0 ]; then
        echo "Ошибка: не удалось создать папку назначения"
        exit 1
    fi
fi

echo ""
echo "Папка назначения: $destination_dir"
echo "Расширение файлов: .$file_extension"

# Поиск всех файлов с указанным расширением в текущей директории
echo "Ищем файлы с расширением .$file_extension в текущей директории..."
files=($(find . -maxdepth 1 -name "*.$file_extension" -type f))

if [ ${#files[@]} -eq 0 ]; then
    echo "Файлы с расширением .$file_extension не найдены в текущей директории."
    exit 0
fi

echo "Найдено ${#files[@]} файлов с расширением .$file_extension"

# Перемещение файлов
moved=0
echo ""
echo "Начинаю перемещение файлов..."

for file in "${files[@]}"; do
    filename=$(basename "$file")
    if mv "$file" "$destination_dir/" 2>/dev/null; then
        echo "✓ Перемещен: $filename"
        ((moved++))
    else
        echo "✗ Ошибка при перемещении: $filename"
    fi
done

echo ""
echo "=========================================="
echo "РЕЗУЛЬТАТЫ ПЕРЕМЕЩЕНИЯ:"
echo "=========================================="
echo "Папка назначения: $destination_dir"
echo "Расширение файлов: .$file_extension"
echo "Всего найдено: ${#files[@]} файлов"
echo "Успешно перемещено: $moved файлов"

if [ $moved -gt 0 ]; then
    echo ""
    echo "Список перемещенных файлов:"
    echo "----------------------------"
    ls -la "$destination_dir"/*.$file_extension
fi

echo ""
echo "Операция завершена!"

