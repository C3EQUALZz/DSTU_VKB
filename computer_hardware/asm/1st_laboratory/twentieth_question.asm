; 20. X = 6*(A - 2*B + C / 4) + 10

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

        mov bx, b
        sal bx, 1       ; bx *= 2

        add ax, bx      ; ax += bx

        mov bx, c       ; bx = c
        sar bx, 2       ; bx /= 4

        add ax, bx      ; ax = A - 2*B + C / 4

        mov bx, 6       ; bx = 6
        mul bx          ; ax = 6 * (A - 2*B + C/4)

        add ax, 10      ; ax = 6 * (A - 2*B + C/4) + 10


        mov x, ax       ; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends

