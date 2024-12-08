.model small
.data
dataArray db 10,0,-12,47,-34,40,50,70,-12,97 ; Пример массива
arraySize equ $-dataArray ; Размер массива

posSum dw 0 ; Сумма положительных чисел
negSum dw 0 ; Сумма отрицательных чисел

.code
start:
    mov ax, @data
    mov ds, ax
    mov cx, arraySize ; Установка счетчика размером массива
    lea si, dataArray ; Загрузка адреса массива в SI

sum_loop:
    cmp cx, 0 ; Проверяем, остались ли элементы в массиве
    je done ; Если элементов не осталось, завершаем цикл

    lodsb ; Загрузка байта в AL и увеличение SI
    cbw ; Преобразование байта в слово (расширение знака)

    test ax, ax ; Проверка знака числа
    jns positive ; Если число положительное (или ноль), перейти к метке 'positive'

negative:
    add negSum, ax ; Добавить число к negSum
    jmp next_element ; Перейти к следующему элементу

positive:
    add posSum, ax ; Добавить число к posSum

next_element:
    dec cx ; Уменьшаем счетчик
    jmp sum_loop ; Перейти к следующему числу

done:
    ; ... (здесь можно добавить код для вывода результатов)

    mov ax, 4C00h ; Завершить программу
    int 21h
end start