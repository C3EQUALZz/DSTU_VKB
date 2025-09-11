#!/bin/bash

echo "Удаление подпапок: group2, group4, ..., group10"
echo "=============================================="

removed_count=0
missing_count=0

for group_num in 2 4 6 8 10; do
	group_name="group$group_num"
	if [ -d "$group_name" ]; then
		rm -rf -- "$group_name"
		if [ $? -eq 0 ]; then
			echo "Удалена папка: $group_name"
			((removed_count++))
		else
			echo "Ошибка при удалении папки: $group_name"
		fi
	else
		echo "Папка $group_name не существует"
		((missing_count++))
	fi
done

echo ""
echo "=========================================="
echo "РЕЗУЛЬТАТЫ УДАЛЕНИЯ:"
echo "=========================================="
echo "Удалено папок: $removed_count"
echo "Отсутствовало папок: $missing_count"

echo "Операция завершена!"
