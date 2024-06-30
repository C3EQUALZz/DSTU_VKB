; В программе имеется циклический счётчик, считающий от 1 до 6. При
; нажатии любой клавиши содержимое счётчика преобразуется в ASCII код и
; выводится в определённое место экрана, после чего счётчик продолжает
; считать. Для анализа нажатия клавиши использовать вектор 1Ch.

JUMPS

.model small
.stack 100h

.data
    WELCOME_MSG db 'Welcome to my Lab 7 program$'
    NEW_LINE db 10, 13, '$'

    DIRECT db 1
    EXIT db 0
    SYM db '@'
    ATRIBUT1 db 14
    ATRIBUT2 db 10
    POS dw 2840
    OLD_CS dw ?
    OLD_IP dw ?
    COUNTER db 1

    DO_DRAW db 0

.code
    extrn putchar:near
    public main

main proc
    mov ax, @data
    mov ds, ax

    show_welcome_msg:
        lea dx, WELCOME_MSG
        mov ah, 09h
        int 21h

    show_new_line:
        lea dx, NEW_LINE
        mov ah, 09h
        int 21h

    ; Чтение вектора прерывания 1Ch
    mov ah, 35h
    mov al, 1Ch
    int 21h

    ; Сохранение старых значений
    mov OLD_IP, bx
    mov OLD_CS, es

    ; Установка нового вектора прерывания 1Ch
    push ds
    mov dx, offset NEW_1C
    mov ax, seg NEW_1C
    mov ds, ax
    mov ah, 25h
    mov al, 1Ch
    int 21h
    pop ds

    mov ax, 0B800h
    mov es, ax
    call CLS
    ; call DELAY

p1:
    cmp EXIT, 0
    jne quit

    cmp COUNTER, 6
    je rerun_cycle

    inc COUNTER
    jmp switch_char

    rerun_cycle:
        mov COUNTER, 1

    switch_char:
        cmp COUNTER, 1
        je char1
        cmp COUNTER, 2
        je char2
        cmp COUNTER, 3
        je char3
        cmp COUNTER, 4
        je char4
        cmp COUNTER, 5
        je char5
        cmp COUNTER, 6
        je char6

        char1:
            mov SYM, 'a'
            jmp end_switch
        char2:
            mov SYM, 'b'
            jmp end_switch
        char3:
            mov SYM, 'c'
            jmp end_switch
        char4:
            mov SYM, 'd'
            jmp end_switch
        char5:
            mov SYM, 'e'
            jmp end_switch
        char6:
            mov SYM, 'f'
            jmp end_switch

        end_switch:
            cmp DO_DRAW, 1
            je draw
            jmp p1

        draw:
            call OUT_SYMBOL
            mov DO_DRAW, 0

    jmp p1

    quit:
        call CLS
        mov dx, OLD_IP
        mov ax, OLD_CS
        mov ds, ax
        mov ah, 25h
        mov al, 1Ch
        int 21h
        mov ah, 4ch
        int 21h

main endp

NEW_1C proc far
    push ax
    push bx
    push cx
    push dx
    push ds
    push es

    mov ax, @data
    mov ds, ax
    mov ax, 40h
    mov es, ax
    mov ax, es:[1ch]
    mov bx, es:[1ah]
    cmp bx, ax
    jne m5
    jmp back
m5:
    mov al, es:[bx]
    mov es:[1ch], bx
    cmp al, 30h
    jnz key_down
    mov EXIT, 1
    jmp back
key_down:
    mov DO_DRAW, 1
    cmp al, 35h
    jne back
    mov dl, ATRIBUT1
    mov dh, ATRIBUT2
    mov ATRIBUT1, dh
    mov ATRIBUT2, dl

back:
    pop es
    pop ds
    pop dx
    pop cx
    pop bx
    pop ax
    iret
NEW_1C endp

CLS proc near
    push cx
    push ax
    push si

    xor si, si
    mov ah, 7
    mov dl, ''
    mov cx, 2000

    CL1:
        mov es:[si], ax
        inc si
        inc si
        loop CL1

    pop si
    pop ax
    pop cx

    ret
CLS endp

DELAY proc near
    push cx
    mov cx, 1
d12:
    push cx
    xor cx, cx
    d11:
        nop
        loop d11
        pop cx
        loop d12
    pop cx
    ret
DELAY endp

OUT_SYMBOL proc near
    push ax
    push bx
    mov al, SYM
    mov ah, ATRIBUT1
    mov bx, POS
    call DELAY
    mov es:[bx], ax
    pop bx
    pop ax
    ret
OUT_SYMBOL endp

end main