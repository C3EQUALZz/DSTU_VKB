#!/bin/bash

echo "Создание структуры папок"
echo "========================"

# Счетчики для отслеживания созданных папок
groups_created=0
users_created=0

echo "Cоздание структуры папок..."

# Создаем папки group1-group10
for group_num in {1..10}; do
    group_name="group$group_num"
    
    # Создаем папку group
    if mkdir -p "$group_name" 2>/dev/null; then
        echo "Создана папка: $group_name"
        ((groups_created++))
        
        # В каждой папке group создаем папки user1-user20
        for user_num in {1..20}; do
            user_name="user$user_num"
            user_path="$group_name/$user_name"
            
            if mkdir -p "$user_path" 2>/dev/null; then
                echo "Создана папка: $user_path"
                ((users_created++))
            else
                echo "Ошибка при создании: $user_path"
            fi
        done
        
        echo ""
    else
        echo "Ошибка при создании папки: $group_name"
    fi
done

echo ""
echo "=========================================="
echo "РЕЗУЛЬТАТЫ СОЗДАНИЯ ПАПОК:"
echo "=========================================="
echo "Создано папок group: $groups_created"
echo "Создано папок user: $users_created"
echo "Общее количество созданных папок: $((groups_created + users_created))"

if [ $groups_created -gt 0 ]; then
    echo ""
    echo "Структура созданных папок:"
    echo "-------------------------"
    for group_num in {1..10}; do
        group_name="group$group_num"
        if [ -d "$group_name" ]; then
            echo "$group_name/"
            for user_num in {1..20}; do
                user_name="user$user_num"
                if [ -d "$group_name/$user_name" ]; then
                    echo "  $user_name/"
                fi
            done
            echo ""
        fi
    done
fi

echo "Операция завершена!"
