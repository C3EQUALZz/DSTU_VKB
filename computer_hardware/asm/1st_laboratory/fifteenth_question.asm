; 15. X = A - 3 * (A + B) + C mod 4

data segment
    a dw 10
    b dw 20
    c dw 8
    x dw ?
data ends

code segment
    assume cs: code, ds: data
    start:
        mov ax, data
        mov ds, ax 		; load addresses

        mov ax, a       ; ax = a
        add ax, b       ; ax += b

        mov bx, -3       ; bx = -3
        mul bx          ; ax *= bx <=> ax *= -3

        add ax, a      ; ax = a - 3 * (a + b)

        mov bx, c        ; bx = c
        and bx, 00000011b ; bx %= 4

        add ax, bx

        mov x, ax 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends