; 6. X = (A/2 + B)/4 + C - 1

data segment
    a dw 10
    b dw 35
    c dw 5
    x dw ?
data ends

code segment
    assume cs: code, ds: data
    start:
        mov ax, data
        mov ds, ax 		; load addresses

        mov ax, a 		; data segment
        sar ax, 1	    ; ax/2

        add ax, b       ; a / 2 + b

        sar ax, 2       ; (a / 2 + b) / 4

        add ax, c       ; (a / 2 + b) / 4 + C

        dec ax

        mov x, ax 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21 			; exit into dos
    end start
code ends