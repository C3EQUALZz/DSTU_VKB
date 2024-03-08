data segment
    array dw 17,0,12,479,-347,40,50,7,4,97
    count dw 0
data ends

code segment
    assume cs: code, ds: data;

start:
     mov ax, data
     mov ds, ax

     lea bx, array
     mov cx, 10

beg:
    mov ax, [bx]
    cmp ax, 10h
    jg GreaterThan10

    jmp next

GreaterThan10:
    add count, 1

next:
    add bx, 2
    loop beg

quit:
    mov ax, 4c00h
    int 21h
code ends
end start