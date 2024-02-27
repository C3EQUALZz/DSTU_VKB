; 1. X = A - 5*(B - 2*C) + 2

data segment
    a dw 10
    b dw 20
    c dw 5
    x dw ?
data ends

code segment
    assume cs: code, ds: data

    start:
        mov ax, data
        mov ds, ax 		; load addresses

        mov ax, c 	    ; ax = c
        mov bx, 2       ; download 2 to bx, because we can't multiply on const
        mul bx          ; ax = 2*C

        mov bx, ax      ; bx = ax = 2 * c
        mov ax, b       ; ax = b
        sub ax, bx      ; ax = b - 2 * C = ax - bx

        mov bx, 5       ; bx = 5
        mul bx          ; ax = 5 * (b - 2*c)

        mov bx, ax      ; bx = 5 * (b - 2*c)
        mov ax, a       ; ax = a
        sub ax, bx      ; ax = ax - bx

        add ax, 2
        mov x, ax       ; record result into x

    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends