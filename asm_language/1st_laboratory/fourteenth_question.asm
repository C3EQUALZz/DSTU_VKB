; 14. X = -(-(C + 2A) * 4B + 38)

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

        mov ax,c        ; ax = c

        mov bx, a       ; bx = a
        sal bx, 1       ; bx = 2 * a

        add ax, bx      ; ax += bx

        neg ax          ; ax *= 1

        mov bx, b       ; bx = b
        sal bx, 2       ; bx *= 4

        mul bx          ; ax = - (C + 2*A) * 4*B
        add ax, 38      ; ax = - (C + 2*A) * 4*B + 38
        neg ax          ; ax = - (-(C + 2*A) * 4*B + 38)

        mov x, ax 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends