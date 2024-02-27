; 2. X= -4A + (B + C)/4 + 2

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
        mov ax, a 		; data segment
        sal ax, 2	    ; ax*2*2 => 4A

        mov bx, b       ; bx = b
        add bx, c       ; bx + c => b + c
        sar bx, 2       ; bx/2*2 => (b + c)/4
        sub bx, ax      ; bx - ax => (b + c)/4 - 4A
        add bx, 2       ; bx + 2 => (b + c)/4 - 4A + 2
        dec bx
        mov x, bx 		; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21 			; exit into dos
    end start
code ends