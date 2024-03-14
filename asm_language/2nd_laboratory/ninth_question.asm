data segment
    array dw 17,0,12,479,-347,40,50,7,4,97 ; 10 16bit elems
    count dw 0 ; counter
data ends

code segment
    assume cs: code, ds: data;

start:
     mov ax, data
     mov ds, ax

     lea bx, array   ;; begin of array
     mov cx, 10      ;; length of array

beg:
    mov ax, [bx]    ;; bx == pointer => data in ax
    cmp ax, 10h     ;; compare with 10 in hex system
    jg GreaterThan10   ;; jump if greater

    jmp next         ;; else

GreaterThan10:
    add count, 1

next:
    add bx, 2
    loop beg         ;; procedure / mark

quit:
    mov ax, 4c00h
    int 21h
code ends
end start
