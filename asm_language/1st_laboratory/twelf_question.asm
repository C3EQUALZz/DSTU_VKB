; 12. X= 6(A - 2B + C/4) + 10

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
        mov ax, a 		; A
        mov bx, b
        sal bx, 1       ; 2B

        sub ax, bx      ; A - 2B
        mov bx, c       ; C
        sar bx, 2       ; C/4
        add ax, bx      ; A-2B + C/4
        mov bx, 6       ; bx = 6
        mul ax          ; 6(A-2B + C/4)
        mov bx, 10      ; bx = 10
        add ax, bx      ;
        mov x, ax 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21 			; exit into dos
    end start
code ends