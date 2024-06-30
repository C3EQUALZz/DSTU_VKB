; 7: Дан массив из 10 байт. Посчитать количество единиц во всех разрядах, кратных трем: 3, 6, 9, ..., 75, 78

segment DATA_S
    buffer db 11011101b, 11111000b
    buffer_s dw $-buffer
DATA_S ends



segment CODE_S
    assume cs:CODE_S, ds:DATA_S

    start:
        mov ax, DATA_S
        mov ds, ax
        mov cx, buffer_s
        mov si, offset buffer
        xor dx, dx

    enumerate_buffer:
        mov al, [si]
        mov ah, 0

        next_bit:
            inc ah
            cmp ah, 9

            jg continue

            shr al, 1
            jc try_inc

            skip_increment_counter:
                jmp next_bit

            try_inc:
                cmp ah, 7
                je increment_counter
                cmp ah, 4
                je increment_counter

            jmp next_bit

            increment_counter:
                inc dx
                jmp next_bit

        continue:
            add si, 1
            loop enumerate_buffer

    quit:
        mov ax, 4c00h
        int 21h
CODE_S ends
end start