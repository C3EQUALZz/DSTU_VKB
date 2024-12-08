; 4. Ввести с клавиатуры строку. Ввести с клавиатуры коротенькую строку - шаблон.
; Найти шаблон во введенной строке. Вывести на экран “ДА”, если шаблон есть и “НЕТ”, если нет.

 DATA_S segment
    str_len db ?
    sub_len db ?
    str_input db 80, ?, 82 dup (?)
    sub_input db 80, ?, 82 dup (?)
    str_prefix db 'Enter string: $'
    sub_prefix db 0dh, 0ah, 'Enter substring: $'
    msg_yes db 0dh, 0ah, 'YES', 0dh, 0ah, 'Index of first entrance: $'
    msg_no db 0dh, 0ah, 'NO$'
    msg_sub_over_error db 0dh, 0ah, 'Error: Substring is longer than string$'
    entrance_idx dw ?
DATA_S ends
CODE_S segment
    assume cs: CODE_S, ds: DATA_S
    ; Decimal number output proc
    WRITENUM proc
        mov ax, entrance_idx
        mov cx, 10
        mov bx, 0
        addition_loop:
            xor dx, dx
            div cx
            add dl, '0'
            push dx
            inc bx
            cmp ax, 0
            jne addition_loop
        print_loop:
            pop dx
            mov ah, 02h
            int 21h
            dec bx
            cmp bx, 0
            jne print_loop
        ret
    WRITENUM endp
    start:
        mov ax, DATA_S
        mov ds, ax
        xor ax, ax  ; Clean ax
        ; Input str_prefix
        mov ah, 09h
        lea dx, str_prefix
        int 21h
        ; Output str_prefix
        mov ah, 0ah
        lea dx, str_input
        int 21h
        ; Input sub_prefix
        mov ah, 09h
        lea dx, sub_prefix
        int 21h
        ; Output sub_prefix
        mov ah, 0ah
        lea dx, sub_input
        int 21h
        mov dh, [str_input + 1]   ; Length of string
        mov str_len, dh
        mov dl, [sub_input + 1]   ; Length of substring
        mov sub_len, dl
        cmp dh, dl
        jb sub_over_error   ; ERROR: Substring longer than string
        lea si, str_input + 2     ; String offset
        lea di, sub_input + 2     ; Substring offset

        mov dh, 0           ; Index of current char
        mov dl, 0           ; Index of first entrance
        mov bl, 0           ; Number of characters found in a row
        mov cl, str_len     ; LOOP (CX)
        next_val:
            inc dh          ; Increase char index
            mov al, [si]
            mov ah, [di + bx]
            inc si          ; Increase char address
            cmp al, ah      ; Comparing current string char
                            ; with indexed substring char
            je equal
        not_equal:
            mov bl, 0       ; Reset counter
            mov dl, 0       ; Reset entrance index
            mov ah, [di]
            cmp al, ah
            je equal
            loop next_val
            jmp no          ; Wasnt found
        equal:
            cmp dl, 0
            jne skip_index  ; If char is not entrance
                mov dl, dh
            skip_index:
            inc bl          ; Increase substring counter
            cmp bl, sub_len ; Substr counter == Length of substring?
            jz yes
            loop next_val
        no:
            mov ah, 09h
            lea dx, msg_no
            int 21h
            jmp quit
        yes:
            mov ah, 09h
            push dx
            lea dx, msg_yes
            int 21h
            pop dx
            mov ah, 0h          ; AX = 00 + entrance_idx
            mov al, dl
            mov entrance_idx, ax
            call WRITENUM
            jmp quit
        sub_over_error:
            mov ah, 09h
            lea dx, msg_sub_over_error
            int 21h
    quit:
        mov ah, 4ch
        int 21h
CODE_S ends
end start