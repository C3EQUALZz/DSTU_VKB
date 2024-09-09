data segment
    prompt1 db 'Enter first string: ',13,10,'$'
    prompt2 db 13,10,'Enter substring: '
    crlf db 13,10,'$'
    txtno db 13,10,'Not '
    txtyes db 'exists $'
    buf1 db 255
    len1 db ?
    str1 db 255 dup (?)
    buf2 db 255
    len2 db ?
    str2 db 255 dup (?)
    counter db ?
data ends

code segment
    assume cs:code,ds:data,ss:stack

    start:
        mov ax,data
        mov ds,ax
        mov es,ax
        mov ah,9
        lea dx,prompt1
        int 21h
        mov ah,10
        lea dx,buf1
        int 21h
        mov ah,9
        lea dx,prompt2
        int 21h
        mov ah,10
        lea dx,buf2
        int 21h
        mov cl,len1
        sub cl,len2
        jb No
        inc cl
        xor ch,ch
        mov counter,ch
        lea di,str1

        m1:
            push cx
            push di
            lea si,str2
            mov cl,len2
            xor ch,ch
            repe cmpsb
            jne m2
            inc byte ptr [counter]

        m2:
            pop di
            inc di
            pop cx
            loop m1
            cmp byte ptr [counter],0
            jne Yes

        No:
            lea dx,txtno
            mov ah,9
            int 21h
            jmp quit

        Yes:
            lea dx,crlf
            mov ah,9
            int 21h
            lea dx,txtyes
            int 21h
            mov al,counter
            xor ah,ah
            mov bx,300Ah
            div bl
            add bh,ah
            xor ah,ah
            div bl
            mov dx,3030h
            add dx,ax
            mov ah,2
            int 21h
            mov dl,dh
            int 21h
            mov dl,bh
            int 21h

        quit:
            mov ah,8
            int 21h
            mov ax,4C00h
            int 21h
code ends

stack segment
    dw 256 dup (?)
stack ends

end start