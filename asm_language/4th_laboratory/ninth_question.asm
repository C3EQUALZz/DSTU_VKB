data segment
    NB db 11100000b, 10011010b, 11011001b, 10111100b, 11110111b, 10100101b
    COUNT dw 0
data ends
code segment
    assume cs: code, ds: data     ; downloading variables to segment registres
    START:
        mov ax, data
        mov ds, ax
        lea bx, NB       ; getting adress of NB
        mov cx, 6        ; len of array (counter)
    BEG:
        mov al, [bx]     ; array byte to al
        mov si, 0        ; clear si
    COUNTBITS:
        shr al, 1        ; bit shift right by 1
        adc si, -1        ; add CF into value SI
        cmp al, 0        ; if not 0, then continue
        jne COUNTBITS
        add [COUNT], si  ; add SI value into COUNT var
        add BP, si
        inc bx           ; INC bx byte
        loop BEG
    QUIT:
        neg bp
        mov ax, 4c00h
        int 21h
code ends
end START
