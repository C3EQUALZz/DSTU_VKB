; 25. X = 5 * A + 2B - B/4 + 131

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
        mov bx, 5       ; bx = 5

        mul bx          ; ax = 5 * a

        mov bx, b       ; bx = b
        sal bx, 1       ; bx = 2*b
        add ax, bx      ; ax = 5 * a + 2*b

        mov bx, b       ; bx = b
        sar bx, 2       ; bx = b / 4

        sub ax, bx      ; ax = 5*a + 2*b - b/4

        add ax, 131     ; ax = 5*a + 2*b - b/4 + 131

        mov x, ax       ; record result into x
    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 	    ; exit into dos
    end start
code ends

