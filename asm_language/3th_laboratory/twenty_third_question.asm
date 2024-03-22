data segment
    array db 01100010b, 01100001b, 01110100b, 10111011b, 10101000b, 10000001b, 10000000b
    countUnit dw 0
    countBytes dw 0
data ends

code segment
    assume cs: code, ds: data

start:
    mov ax, data
    mov ds, ax

    lea bx, array
    mov cx, 7

beg:
    mov al, [bx]
    mov countUnit, 0

coutnn:
    test al, 1
    jz zeroBit
    inc countUnit

zeroBit:
    shr al, 1
    jnz coutnn

    cmp countUnit, 3
    jg next
    inc countBytes

next:
    add bx, 1
    loop beg

quit:
    mov ax, 4C00h
    int 21h

END start
