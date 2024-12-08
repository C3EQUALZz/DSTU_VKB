.model small
.stack 100h

.data
    ; arr db 11110010b, 10010001b, 11111111b, 10101010b, 11010101b, 10000001b, 10111101b  ; answer is 5
    arr db 01100101b, 10101010b, 11100001b, 00011011b, 01010101b, 11011000b, 00110011b  ; answer is 6
    zeroes_count db 0
    bits_count db 0

.code
    mov ax, @data
    mov ds, ax
    xor ax, ax
    xor bx, bx
    xor cx, cx
    xor dx, dx

    mov si, 0  ; bytes count
    mov bl, 7  ; chech for end of 7 bit word
    mov bh, 8  ; check for end of byte
    mov dl, 2  ; check for odd number of zeroes
    mov di, 0  ; count of words with odd number of zeroes


byte_loop:
    mov dh, 10000000b
    mov cl, arr[si]

bit_loop:
    test cl, dh
    jnz middle_part
    inc zeroes_count
middle_part:
    xor ax, ax
    inc bits_count
    mov al, bits_count
    div bl
    cmp ah, 0
    jne end_part
    xor ax, ax
    mov al, zeroes_count
    mov zeroes_count, 0
    div dl
    cmp ah, 1
    jne end_part
    inc di
end_part:
    xor ax, ax
    mov al, bits_count
    div bh
    cmp ah, 0
    je next_byte

    shr dh, 1
    jmp bit_loop

next_byte:
    inc si
    cmp si, 7
    je prog_end
    jmp byte_loop

prog_end:
    mov ax, di  ; answer is put into al
    mov ah, 4ch
    int 21h