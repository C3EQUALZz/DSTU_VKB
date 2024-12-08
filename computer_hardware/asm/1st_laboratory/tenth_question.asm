; 10. X = 2 * B - 1 + 4 * (A - 3 * C)

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

        mov bx, b       ; bx = b
        sal bx, 1       ; bx *= 2
        dec bx          ; bx -= 1

        mov ax, c       ; ax = c
        mov cx, 3       ; cx = 3
        mul cx          ; ax = 3 * c
        neg ax          ; ax = (3 * c) * (-1)
        add ax, a       ; ax = a - 3*c
        sal ax, 2       ; ax = (a - 3*c) * 4

        add ax, bx      ; ax = (a - 3*c) * 4 + 2b - 1

        mov x, ax 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends