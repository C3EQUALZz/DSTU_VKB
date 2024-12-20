.data
massiv db 10000000b         ; Инициализируем массив massiv с одним байтом (10000000b)

.code
     mov dx, 0              ; Обнуляем регистр DX (используется для подсчета значений)
     mov bx, 5              ; Устанавливаем BX в 5 (индекс для работы с массивом)

a0:
     mov ah, 0              ; Обнуляем AH (используется для хранения промежуточного результата)
     mov al, massiv[bx]     ; Загружаем байт из массива massiv по индексу BX в AL
     mov cx, 8              ; Устанавливаем CX в 8 (количество бит для обработки)

a1:
     shr al, 1              ; Сдвигаем AL вправо на 1 бит (делим на 2)
     adc ah, 0              ; Добавляем к AH значение переноса (если есть) от предыдущего сдвига
     loop a1                ; Уменьшаем CX и повторяем цикл, пока CX не станет 0

     cmp ah, 3              ; Сравниваем значение в AH с 3
     ja a2                  ; Если AH больше 3, переходим к метке a2

     inc dx                 ; Увеличиваем DX на 1, если значение в AH меньше или равно 3

a2:
     dec bx                 ; Уменьшаем BX для перехода к следующему элементу массива
     jns a0                 ; Если BX не отрицателен, продолжаем цикл (пока BX >= 0)
