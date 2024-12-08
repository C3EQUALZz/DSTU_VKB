data segment
    prompt1 db 'Enter first string: $'
    prompt2 db 13,10,'Enter substring: $'
    crlf db 13,10,'$'
    txtno db 13,10,'Not '
    txtyes db 'exists $'
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
        mov ah,9 ; вывод строки на экран
        lea dx,prompt1 ; первый промт для вывода на экран
        int 21h ; системное прерывание для 1 считывания с консоли
        mov ah,10 ; считвание строки с консоли
        lea dx,buf1 ; сохраняем данные с консоли
        int 21h ; вызываем в консоль с последующим сохранением в dx
        mov ah,9 ; вывод строки на экран
        lea dx,prompt2 ; второй промпт для вывода на экран
        int 21h ; вызов консоли
        mov ah,10 ; cчитывание строки
        lea dx,buf2 ; переносим в buf2
        int 21h ; системное прерывание для считывания 2 строки с консоли
        mov cl,len1
        sub cl,len2
        jb No
        inc cl
        xor ch,ch
        mov counter,ch
        lea di,str1

    m1:
        push cx ; сохраняем значение в стеке
        push di ; сохраняем значение в стеке
        lea si,str2 ; загружается адрес второй строки в регистр SI
        mov cl,len2 ; в CL устанавливается длина второй строки.
        xor ch,ch ; обнуляем
        repe cmpsb ; сравниваются байты у SI и DI
        jne m2 ; если не равны, то идет на m2
        inc byte ptr [counter] ; если равны, то увеличиваем значение счетчика

    m2:
        pop di ; восстановление значений из стека
        inc di ;
        pop cx
        loop m1
        cmp byte ptr [counter],0
        jne Yes

    No:
        lea dx,txtno ; отдаем адрес в регистр
        mov ah,9 ; вывод строки на экран
        int 21h ; вызов консоли
        jmp quit ; покидаем программу

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
    dw 256 dup (?) ; double word (2 байта), в x86 архитектуре тут 2 байта
stack ends

end start