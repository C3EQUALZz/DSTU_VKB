; 11. X = (2*A + B) / 4 - C / 2 + 168

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
        sal ax, 1       ; ax = a * 2
        add ax, b       ; ax = a * 2 + b
        sar ax, 2       ; ax = (a * 2 + b) / 4

        mov bx, c       ; bx = c
        sar bx, 1       ; bx = c / 2

        sub ax, bx      ; ax = (a * 2 + b) / 4 - c / 2

        add ax, 168     ; ax = (a * 2 + b) / 4 - c / 2 + 168

        mov x, ax 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends