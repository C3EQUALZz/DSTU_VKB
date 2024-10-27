.model small
.stack 100h
.data
    buffer db 50 dup('$')
    maxlen db 20
    output db 50 dup('$')
    strlen db 0
    flag db 0
    newline db 0dh, 0ah, '$'

.code
start:
    mov ax, @data
    mov ds, ax

    mov dx, offset buffer
    mov ah, 0ah
    int 21h

    mov dx, offset newline
    mov ah, 09h
    int 21h

    mov si, offset buffer
    mov bl, [si+1]
    mov [strlen], bl

    cmp bl, maxlen
    jl stretch
    jg trim

    mov dx, offset buffer + 2
    mov ah, 09h
    int 21h

    jmp end_program

trim:
    mov bl, maxlen
    mov [si+1], bl

    lea di, buffer
    mov al, maxlen
    mov ah, 0
    add di, ax
    add di, 2

    mov [di], '$'

    mov dx, offset buffer + 2
    mov ah, 09h
    int 21h

    jmp end_program

stretch:
    mov al, maxlen
    mov ah, 0
    mov cx, ax

    mov bl, [strlen]
    sub cx, bx

    mov di, offset output
    mov si, offset buffer + 2
    mov bx, cx

    mov strlen, 0

next_char:
    cmp [si], 20h
    jne write_char
    call insert_spaces
middle:
    inc si
    cmp strlen, 14
    jne next_char
    jmp output_string

write_char:
    mov al, [si]
    mov [di], al
    inc si
    inc di
    inc strlen
    jmp next_char

insert_spaces:
    mov cx, bx
    mov al, ' '
    mov [di], al
    inc di
    cmp flag, 1
    je middle
write_space:
    mov [di], al
    inc di
    dec cx
    inc strlen
    mov flag, 1
    cmp cx, 0
    jne write_space
    ret

output_string:
    mov dx, offset output
    mov ah, 09h
    int 21h

end_program:
    mov ah, 4ch
    int 21h

end start
