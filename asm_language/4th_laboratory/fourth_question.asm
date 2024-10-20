.model tiny
.code
    org 100h
start:
    mov si, offset mas
    mov cx, 10
    xor dl, dl
mainloop:
    lodsb
    xor ah, ah
calc:
    shr al, 1
    adc ah, 0
    or  al, al
    jnz calc
    xor ah, 3
    sub ah, 1
    adc dl, 0
    loop    mainloop
    xor ah, ah
    mov al, dl
    aaa
    rol ax, 8
    or  ax, 3030h
    mov word ptr x, ax
    mov dx, offset otvet
    mov ah, 9
    int 21h
    ret
;----------------------------------
mas db  2,3,1011011b,255,34,82,234,1,51,0
otvet   db  'in massiv '
x   db  '00 byte with number 1-s in byte equal 3$'
;----------------------------------
    end start