data segment
    mass db 10101010b,11111111b,0101010b, 11111111b, 10101010b, 11111111b,11111111b, 11111111b, 11111111b
data ends
code segment
assume cs: code, ds:data
START:
    mov ax, data
    mov ds, ax

    xor ax, ax
    xor bx, bx
    lea si, [mass]
    mov bl, [si]        ;PrevBit:=(a[0] and 1);
    and bl, 1
    mov dx, 0           ;Count:=0;
    mov cx, 9           ;for i:=0 to 8 do
    forI:
        mov al, [si]    ;  X:=a[i]
        push cx
        mov cx, 8       ;  for j:=0 to 7 do
        forJ:
            mov di, ax  ;    Count:=Count+ ((X xor PrevBit) and X and 1);
            xor di, bx
            and di, ax
            and di, 1
            add dx, di
            mov bl, al  ;    PrevBit:= X and 1;
            and bl, 1
            shr al, 1   ;    X:=X shr 1;
        loop forJ
        pop cx
        inc si
    loop forI
    mov ax, dx

xor ax, ax
mov ax, 4c00h ; ??? ?????????? 0
Int 21h ; ????? ? DOS
code ends
end START
1