#!/bin/bash

echo "Программа для удаления файлов по расширению"
echo "=========================================="

# Запрашиваем путь к директории
echo -n "Введите путь к директории (или Enter для текущей): "
read target_dir

# Если путь не указан, используем текущую директорию
if [ -z "$target_dir" ]; then
    target_dir="."
fi

# Проверяем, существует ли директория
if [ ! -d "$target_dir" ]; then
    echo "Ошибка: директория '$target_dir' не существует!"
    exit 1
fi

echo "Целевая директория: $target_dir"

# Получение расширения от пользователя
echo -n "Введите расширение файлов для удаления: "
read extension

# Убираем точку в начале, если пользователь её указал
extension=${extension#.}

# Поиск файлов с указанным расширением в указанной директории
files=($(find "$target_dir" -maxdepth 1 -name "*.${extension}" -type f))

if [ ${#files[@]} -eq 0 ]; then
    echo "Файлы с расширением '$extension' не найдены в директории '$target_dir'."
    exit 0
fi

echo "Найдено ${#files[@]} файлов с расширением '$extension' в директории '$target_dir'"

# Подтверждение удаления
echo -n "Удалить все файлы? (да/нет): "
read confirm

if [[ $confirm == "да" || $confirm == "yes" || $confirm == "y" || $confirm == "д" ]]; then
    deleted=0
    
    for file in "${files[@]}"; do
        if rm "$file" 2>/dev/null; then
            echo "Удален: $(basename "$file")"
            ((deleted++))
        else
            echo "Ошибка при удалении: $(basename "$file")"
        fi
    done
    
    echo "Успешно удалено: $deleted файлов"
else
    echo "Операция отменена."
fi
