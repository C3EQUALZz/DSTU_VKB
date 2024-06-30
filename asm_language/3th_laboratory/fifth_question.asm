; Вариант 5: Найти количество положительных чисел. Массив байт.

DATA_S segment
msg db 'Amount of positive values: $'
val dw 0
buff db 10, 24, 50, 43, -20, -25, 4, 70, -124, -97   ; 6 положительных чисел
buff_s dw 10
DATA_S ends
CODE_S segment
    assume cs: CODE_S, ds: DATA_S
    ; Вывод строки
    WRITESTR proc
        xor ax, ax
        mov ah, 09h
        lea dx, msg
        int 21h
        ret
    WRITESTR endp

    ; Вывод значения
    WRITENUM proc
        mov ax, val
        mov cx, 10          ; Делитель - система счисления
        mov bx, 0           ; Счетчик цифр в числе
        addition_loop:
            xor dx, dx      ; Очистить регистр dx
            div cx          ; Получаем остаток от деления на СС -> Последняя цифра
            add dl, '0'     ; Добавляем 0 для конца символа
            push dx
            inc bx
            cmp ax, 0
            jne addition_loop
        print_loop:
            pop dx          ; Вытаскиваем число
            mov ah, 02h     ; Вывод на дисплей
            int 21h         ; одного символа
            dec bx
            cmp bx, 0
            jne print_loop
        ret
    WRITENUM endp
    ; Ввод символа (пауза)
    READC proc
        mov ah, 07h
        int 21h
        ret
    READC endp
    start:
        mov ax, DATA_S
        mov ds, ax
        mov ax, 0h
        mov bx, offset buff
        mov cx, buff_s      ; Размер массива чисел
    check_val:
        mov al, [bx]
        test al, al
        js next_val         ; Если число отрицательное берем следующий элемент
    not_negative:
        inc val             ; Увеличиваем счетчик положительных чисел
    next_val:
        inc bx              ; Переход на следующий элемент
        loop check_val
        call WRITESTR
        call WRITENUM
        call READC
    quit:
        mov ax, 4c00h
        int 21h
CODE_S ends
end start