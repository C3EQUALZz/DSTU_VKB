.model small
.stack 100h
.data
    data_array db 11111111b, 11111111b, 11111111b, 11101110b, 01010101b, 01111101b, 01011001b, 01110000b
    max_count dw 0
.code
.startup

    xor bx, bx  ; индекс текущего байта в массиве
    mov bx, 7
    xor cx, cx  ; счетчик для текущей последовательности единиц
    xor dx, dx  ; индекс текущего бита в байте

loop_bytes:  ; начало цикла, который будет обрабатывать каждый байт массива data_array
    mov al, data_array[bx]

loop_bits:  ; начало вложенного цикла, который будет перебирать биты внутри текущего байта.
    test al, 1
    jz reset_count
    inc cx

    cmp cx, max_count
    jbe skip
    mov max_count, cx

skip:
    shr al, 1
    inc dx
    cmp dx, 8
    jne loop_bits

    xor dx, dx
    dec bx
    cmp bx, -1
    jne loop_bytes

    mov ax, max_count
    .exit

reset_count:
    xor cx, cx
    jmp skip
