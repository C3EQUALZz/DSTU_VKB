; 21. X = 3 * (A - 4 * B) + C / 4

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

        mov bx, b       ; bx = b
        sal bx, 2       ; bx *= 4

        sub ax, bx      ; ax = a - 4*b

        mov bx, 3       ; bx = 3
        mul bx          ; 3 * (a - 4*b)

        mov bx, c       ; bx = c
        sar bx, 2       ; bx = c / 4

        add ax, bx      ; ax = 3 * (a - 4*b) + c / 4


        mov x, ax       ; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends

