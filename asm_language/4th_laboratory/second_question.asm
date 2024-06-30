; Дан массив из 8 байт. Рассматривая его, как массив из 64 бит, посчитать количество единиц.

data segment
    NB db 04h, 07h, 14h, 23h, 04h, 38h, 3Fh, 2Ah
    COUNT dw 0
data ends
code segment
    assume cs: code, ds: data
START:
    mov ax, data
    mov ds, ax
    lea bx, NB
    mov cx, 8        ; len of array (counter)
BEG:
    mov al, [bx]     ; array byte to al
    mov si, 0        ; clear si
COUNTBITS:
    shr al, 1        ; bit shift right by 1
    adc si, 0        ; add CF into value SI
    cmp al, 0        ; if not 0, then continue
    jne COUNTBITS
    add [COUNT], si  ; add SI value into COUNT var
    inc bx           ; INC bx byte
    loop BEG
QUIT:
    mov ax, 4c00h
    int 21h
code ends
end START
