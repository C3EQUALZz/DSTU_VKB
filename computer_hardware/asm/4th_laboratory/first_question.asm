data segment
K db ?                    ; kol vo byte v kotorix sbroheni 6 i 4 byte
NB db 04h, 07h, 14h, 23h, 04h,38h,3Fh, 2Ah,0Dh, 34h
data ends

code segment

    assume cs: code, ds:data

    START:
            mov     ax, data
            mov     ds, ax
            lea     bx, NB
            mov     cx, 10
            xor     ax, ax
    BEG:
            mov     al, [bx]
            test    al, 1010000b
            jnz     NEXT
            inc     ah
    NEXT:
            inc     bx
            loop     BEG
            mov     K, ah
    QUIT:
            mov     ax, 4c00h
            Int     21h

code        ends
end         START