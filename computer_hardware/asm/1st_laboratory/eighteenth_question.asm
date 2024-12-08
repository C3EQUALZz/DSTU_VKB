; 18. X = 3*(C - 2*A) + (B - C + 1) / 2

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
        sal ax, 1       ; ax *= 2 <=> ax = 2*a
        neg ax          ; ax = -2*a

        add ax, c       ; ax = -2*a + c

        mov bx, 3
        mul bx          ; ax = 3 * (c - 2*a)

        mov bx, b       ; bx = b
        sub bx, c       ; bx = b - c
        inc bx          ; bx = b - c + 1
        sar bx, 1       ; bx = (b - c + 1) / 2

        add ax, bx      ; ax = 3*(c - 2*a) + (b - c + 1) / 2

        mov x, ax       ; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends

