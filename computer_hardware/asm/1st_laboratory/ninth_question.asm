; 9. X = 2 - B * (A + B) + C / 4

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
        add ax, b       ; a + b => ax += b
        mov bx, b       ; bx = b (for multiply)
        mul bx          ; ax *= bx

        xchg bx, ax     ; swap(bx, ax) cause i want ax = 2

        mov ax, 2
        sub ax, bx      ; ax = 2 - B(A + B)

        mov bx, c       ; bx = c
        sar bx, 2       ; bx = c / 4

        add ax, bx

        mov x, ax 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends