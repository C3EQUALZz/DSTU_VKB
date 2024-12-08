; 16. X = 3 * (A - 2*B) + 50 - C / 2

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

        mov bx, b       ; bx = b
        sal bx, 1       ; bx *= 2

        sub ax, bx      ; ax = a - 2*b

        mov bx, 3       ; bx = 3
        mul bx          ; ax = 3 * (a - 2*b)

        add ax, 50      ; ax = 3 * (a - 2*b) + 50

        mov bx, c       ; bx = c
        sar bx, 1       ; bx = c / 2

        sub ax, bx      ; ax = 3 * (a - 2*b) + 50 - c / 2

        mov x, ax 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends