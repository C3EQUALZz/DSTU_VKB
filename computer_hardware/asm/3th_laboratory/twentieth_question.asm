; 20: Найти среднее арифметическое чисел больших 10. Массив слов.

DATA_S segment
    buffer dw 1, 10, 12, -4, -50, 8, 14
    buffer_s dw $-buffer
    sum dw 0h
    count dw 0h
DATA_S ends

CODE_S segment
    assume cs:CODE_S, ds:DATA_S

    start:
        mov ax, DATA_S
        mov ds, ax
        mov ax, buffer_s
        sar ax, 1
        mov cx, ax
        mov si, offset buffer

    enumerate_buffer:
        mov ax, [si]
        cmp ax, 10
        jg greater

        jmp continue

        greater:
            add sum, ax
            inc count

        continue:
            add si, 2
            loop enumerate_buffer

    mean_to_ax:
        mov ax, sum
        div count

    quit:
        mov ax, 4c00h
        int 21h
CODE_S ends
end start