section .data
    array db -33, 47, 118, -53, 93, 89, -32
    array_length equ $ - array
section .text
global main:
    mov ebp, esp
main:
    mov ecx, array_length ; Кол-во элементов в массиве
    lea esi, [array] ; Загрузка адреса начала массива
process_array:
    mov al, [esi]
    test al, 0x80 ; Проверка старшего бита на знак
    jz next ; Если старший бит не установлен, число положительное, переходим к следующему элементу
    neg al
    mov [esi], al
next:
    inc esi ; след элемент
    loop process_array ; Повторение цикла для всех элементов массива
    ; Вывод массива в консоль
    mov eax, 4 ; Системный вызов write
    mov ebx, 1 ; Файловый дескриптор stdout
    mov ecx, array
    mov edx, array_length
    int 0x80
    mov eax, 1
    xor ebx, ebx
    int 0x80
