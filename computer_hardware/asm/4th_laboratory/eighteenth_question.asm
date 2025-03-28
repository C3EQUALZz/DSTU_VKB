org 100h                     ; Указываем, что код начинается с адреса 100h (для .COM файлов)

begin:
    jmp start                ; Переходим к метке start
    db "*"                   ; Символ, который будет использован в качестве разделителя
    NB db 10100111b, 11111100b, 10010010b ; Исходные данные (массив байтов)
    db "*"                   ; Символ, который будет использован в качестве разделителя
    xorop db 10100000b, 0, 0    ; Инициализируем массив xorop (первый байт - 101, остальные - 0)

start:
    call doxor               ; Вызываем процедуру doxor для выполнения операции XOR
    ; call doxor            ; Закомментированная строка для повторного вызова doxor (можно раскомментировать)
    ret                      ; Возвращаемся из программы

doxor:
    mov bl, 10100000b       ; Загружаем 101 в BL (первый байт для операции XOR)
    mov bh, 0                ; Обнуляем BH (второй байт для операции XOR)
    lea di, xorop           ; Загружаем адрес массива xorop в DI
    mov [di], bl            ; Сохраняем значение BL в первый байт xorop
    mov [di + 1], bh        ; Сохраняем значение BH во второй байт xorop
    mov [di + 2], bh        ; С��храняем значение BH в третий байт xorop
    mov cx, 8                ; Устанавливаем CX в 8 (количество итераций для цикла)

m0:
    lea si, NB              ; Загружаем адрес массива NB в SI
    mov al, [di]            ; Загружаем первый байт из xorop в AL
    xor [si], al            ; Выполняем операцию XOR между первым байтом NB и AL

    mov al, [di + 1]        ; Загружаем второй байт из xorop в AL
    xor [si + 1], al        ; Выполняем операцию XOR между вторым байтом NB и AL

    mov al, [di + 2]        ; Загружаем третий байт из xorop в AL
    xor [si + 2], al        ; Выполняем операцию XOR между третьим байтом NB и AL

    clc                      ; Обнуляем флаг переноса перед циклическим сдвигом
    rcr byte ptr [di], 1    ; Циклически сдвигаем первый байт xorop вправо на 1 бит
    rcr byte ptr [di + 1], 1; Циклически сдвигаем второй байт xorop вправо на 1 бит
    rcr byte ptr [di + 2], 1; Циклически сдвигаем третий байт xorop вправо на 1 бит

    clc                      ; Обнуляем флаг переноса перед циклическим сдвигом
    rcr byte ptr [di], 1    ; Циклически сдвигаем первый байт xorop вправо на 1 бит
    rcr byte ptr [di + 1], 1; Циклически сдвигаем второй байт xorop вправо на 1 бит
    rcr byte ptr [di + 2], 1; Циклически сдвигаем третий байт xorop вправо на 1 бит

    clc                      ; Обнуляем флаг переноса перед циклическим сдвигом
    rcr byte ptr [di], 1    ; Циклически сдвигаем первый байт xorop вправо на 1 бит
    rcr byte ptr [di + 1], 1; Циклически сдвигаем второй байт xorop вправо на 1 бит
    rcr byte ptr [di + 2], 1; Циклически сдвигаем третий байт xorop вправо на 1 бит

    loop m0                 ; Уменьшаем CX и повторяем цикл, пока CX не станет 0
    ret                     ; Возвращаемся из процедуры doxor
