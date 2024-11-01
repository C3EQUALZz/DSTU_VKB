.model small
.stack 100h

.data
    arr db 00110001b, 00110010b, 00000011b, 00010100b, 11010101b, 01100110b, 00000101b, 00011000b, 00101001b, 01000000b, 01010001b
    byte_count db 0
    flag db 0

.code
    mov ax, @data
    mov ds, ax

    mov cx, 11
    mov bx, 0


byte_loop:
    mov al, arr[bx]
    mov si, 0

bit_loop:
    test al, 1
    jnz capture
    mov flag, 0
middle:
    inc si
    shr al, 1
    cmp si, 8
    jne bit_loop
    inc byte_count
    jmp skip

capture:
    cmp flag, 1
    je skip
    mov flag, 1
    jmp middle

skip:
    mov flag, 0
    inc bx
    loop byte_loop
    mov al, byte_count
    mov ah, 4ch
    int 21h