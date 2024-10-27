.model small
.stack 100h

.data
    arr db 11010010b, 10010001b, 11111111b, 10101010b, 11010101b, 10000001b, 10111101b, 10001101b, 01010101b, 01001011b
    ones_count db 0
    all_bits_count db 0

.code
    mov ax, @data
    mov ds, ax

    mov si, 0  ; number of bytes
    mov cx, 0   ; number of bits
    mov bl, 3   ; multiple

    xor ax, ax

byte_loop:
    mov dl, 10000000b
    mov al, arr[si]
    mov cx, 0

bit_loop:
    test al, dl
    jnz check_multiple
    push ax
    xor ax, ax
middle:
    pop ax
    inc all_bits_count

    inc cx
    cmp cx, 8
    je next_byte

    shr dx, 1
    jmp bit_loop

next_byte:
    inc si
    cmp si, 10
    je end
    jmp byte_loop

check_multiple:
    push ax
    xor ax, ax
    mov al, all_bits_count
    div bl        ; AX / 3
    cmp ah, 0
    je plus_one
    jmp middle

plus_one:
    inc ones_count
    jmp middle

end:
    mov al, ones_count
    mov ah, 4ch
    int 21h