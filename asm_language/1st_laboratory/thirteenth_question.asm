; 13. X = 5 * (A - B) + C mod 4

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
        sub ax, b       ; ax = a - b

        mov bx, 5
        mul bx          ; ax = (a - b) * 5

        mov bx, c       ; bx = c
        and bx, 00000011b ; mod 4, last 2 bits => remainder of the division by 4

        add ax, bx

        mov x, ax 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends