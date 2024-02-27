; 4. X = - A / 2 + 4 * (B + 1) + 3*C

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

        mov cx, a       ; cx = a
        sar cx, 1       ; a / 2
        neg cx          ; - a / 2

        mov ax, b       ; ax = b
        mov bx, 4       ; coeff 4 for 4*(b+1)
        inc ax          ; ax + 1 => b + 1
        mul bx          ; 4 * (b+1)

        add cx, ax      ; - a / 2 + 4*(b+1)

        mov ax, c       ; ax = c
        mov bx, 3       ; bx = 3
        mul bx          ; ax = 3 * c

        add cx, ax      ; -a/2 + 4*(b+1) + 3*c

        mov x, cx       ; record result into x

    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends

