.model small
.stack 100h
.data
    data_array db 11111111b, 11111111b, 11111111b, 11101010b, 01010101b, 01111101b, 01011001b, 01110001b
    zero_counter dw 0
.code
.startup

    mov ax, 0
    xor bx, bx
    mov bx, 7
    xor cx, cx
    xor dx, dx

loop_bytes:
    mov al, data_array[bx]

loop_bits:
    test al, 1
    jz negative

    jmp positive

skip:
    shr al, 1
    inc dx
    cmp dx, 8
    jne loop_bits

    xor dx, dx
    dec bx
    cmp bx, -1
    jne loop_bytes

    .exit

positive:
    mov cx, 1
    jmp skip

negative:
    cmp cx, 1
    je counter

    jmp skip

counter:
    inc ah
    mov cx, 0
    jmp skip