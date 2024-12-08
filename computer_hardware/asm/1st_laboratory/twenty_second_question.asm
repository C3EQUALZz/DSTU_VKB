; 22. X = -(-(C + 2*A) * 5*B - 27)

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

        mov ax, a       ; ax = a

        sal ax, 1       ; ax = 2 * a
        add ax, c       ; ax = c + 2*a

        neg ax          ; ax = - (C + 2*A)

        mov bx, b       ; bx = b
        mul bx          ; ax = - (C + 2*A) * bx
        mov cx, 5       ; cx = 5
        mul cx          ; ax = - (C + 2*A) * bx * 5

        sub ax, 27      ; ax = - (C + 2*A) * bx * 5 - 27

        neg ax          ; ax = - (-(C + 2*A) * bx * 5 - 27)

        mov x, ax       ; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends

