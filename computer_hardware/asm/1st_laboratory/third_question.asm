; 3. X = 7*A - 2*B - 100 + C

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
        mov bx, 7       ; bx = 7
        mul bx          ; ax *= bx

        mov bx, ax      ; bx = ax
        mov ax, 2       ; ax = 2
        mov cx, b       ; cx = b
        mul cx          ; ax = 2*B

        sub bx, ax      ; 7*A - 2*B
        sub bx, 100     ; 7*A - 2*B - 100
        add bx, c       ; 7*A - 2*B - 100 + C

        mov x, bx       ; record result into x

    quit:
        mov ax, 4c00h 	; end code 0
        int 21h 			; exit into dos
    end start
code ends