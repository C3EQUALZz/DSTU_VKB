#!/bin/bash

# Выполняем команду ls -l /dev и сохраняем вывод в переменную
output=$(ls -l /dev)

# Инициализируем массивы для различных типов файлов
declare -a directories
declare -a symlinks
declare -a char_devices
declare -a block_devices
declare -a named_pipes
declare -a sockets

# Перебираем строки вывода
while IFS= read -r line; do
  # Извлекаем первый символ строки (тип файла)
  file_type=${line:0:1}

  # Добавляем строку в соответствующий массив
  case $file_type in
    'd')
      directories+=("$line")
      ;;
    'l')
      symlinks+=("$line")
      ;;
    'c')
      char_devices+=("$line")
      ;;
    'b')
      block_devices+=("$line")
      ;;
    'p')
      named_pipes+=("$line")
      ;;
    's')
      sockets+=("$line")
      ;;
  esac
done <<< "$output"

# Выводим результаты
printf "\nDirectories:\n"
for dir in "${directories[@]}"; do
  echo "$dir"
done

printf "\nSymbolic Links:\n"
for link in "${symlinks[@]}"; do
  echo "$link"
done

printf "\nCharacter Devices:\n"
for char_dev in "${char_devices[@]}"; do
  echo "$char_dev"
done

printf "\nBlock Devices:\n"
for block_dev in "${block_devices[@]}"; do
  echo "$block_dev"
done

printf "\nNamed Pipes:\n"
for pipe in "${named_pipes[@]}"; do
  echo "$pipe"
done

printf "\nSockets:\n"
for socket in "${sockets[@]}"; do
  echo "$socket"
done
