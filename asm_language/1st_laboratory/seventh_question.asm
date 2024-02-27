; 7. X = -(C + 2A + 4B + B)

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

        mov ax, c 		; ax = c

        mov bx, a       ; bx = a
        sal bx, 1       ; bx *= 2

        add ax, bx      ; c += 2a

        mov bx, b       ; bx = b
        sal bx, 2       ; bx *= 4
        add bx, b       ; bx += b

        add ax, bx       ; cx = c + 2a + 5b

        neg ax          ; cx = - (c + 2a + 5b)

        mov x, ax 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends