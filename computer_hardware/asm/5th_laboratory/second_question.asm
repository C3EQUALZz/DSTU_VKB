.model small
.data
    str1 db 80, ?, 80 dup ("$")
    msg1 db ' Input string: $'
    msg2 db 0Dh, 0Ah, ' Output: $'

.code
    mov ax, @data
    mov ds, ax

    ; ask input (stdout)
    lea dx, msg1
    mov ah, 09h    ; view data into screan
    int 21h        ; inerapt

    ; ask stdin
    lea dx, str1
    mov ah, 0Ah
    int 21h


    xor ax, ax  ; clear

    lea di, str1 + 2 ; pointer
    xor cx, cx  ; counter
    mov cl, [str1 + 1] ; str + 1 -> len of str in 2 byte


beg:
    cmp [di], 91
    jb lo

    cmp [di], 123
    jge lo

    cmp [di], 97
    jbe lo


    sub [di], 32



lo:
    ; loop
    inc di
    loop beg

next:
    ; finally
    lea dx, msg2
    mov ah, 09h
    int 21h

    ; finally
    lea dx, str1 + 2
    mov ah, 09h
    int 21h



exit:
    mov ah, 4Ch
    int 21h
end