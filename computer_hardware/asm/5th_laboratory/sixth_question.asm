.model small
.stack 100h
.data
    inputstr db 100 dup('$')     ; buffer for the input string
    outputstr db 100 dup('$')    ; buffer for the output string
    temparr db 20 dup('$')       ; array for storing characters of the current word
    msginput db 'Enter string: $'
    msgoutput db 'Reversed string: $'
    newline db 0dh, 0ah, '$'

.code
start:
    ; Initialize segments
    mov ax, @data
    mov ds, ax

    ; Request the string from the user
    lea dx, msginput
    mov ah, 09h
    int 21h

    lea dx, inputstr
    mov ah, 0ah        ; Input string
    int 21h

    ; Print a new line
    lea dx, newline
    mov ah, 09h
    int 21h

    ; Start processing the string
    mov si, 2          ; SI points to the first character in the buffer (index 2 after length byte)
    mov di, 0          ; DI points to the position in the output string
    mov bx, 0          ; BX is used to track the position in temparr

next_char:
    mov al, inputstr[si]   ; Read the current character
    cmp al, 0dh            ; Check for end of string (Enter pressed)
    je process_word_end     ; Process the last word before output

    cmp al, ' '            ; Check if the character is a space
    je process_word        ; If it's a space, process the accumulated word

    ; If it's not a space, save the character in temparr
    mov temparr[bx], al
    inc bx
    inc si
    jmp next_char

process_word:
    ; Process the accumulated word in temparr, writing it in reverse order to outputstr
    dec bx                 ; Set BX to point to the last character
    jz continue            ; Skip if the word is empty
reverse_loop:
    mov al, temparr[bx]
    mov outputstr[di], al
    inc di
    dec bx
    jns reverse_loop        ; Repeat while BX >= 0

    ; Add a space after the reversed word
continue:
    mov outputstr[di], ' '
    inc di
    mov bx, 0               ; Reset BX for the next word
    inc si                  ; Move to the next character in the input string
    jmp next_char

process_word_end:
    ; If the end of the string is reached, process the last word
    dec bx                 ; Set BX to point to the last character
    jz output_string        ; Skip if the word is empty
reverse_loop_end:
    mov al, temparr[bx]
    mov outputstr[di], al
    inc di
    dec bx
    jns reverse_loop_end    ; Repeat while BX >= 0

    ; Proceed to output the string
output_string:
    ; Output the reversed string
    lea dx, msgoutput
    mov ah, 09h
    int 21h

    lea dx, outputstr
    mov ah, 09h
    int 21h

    ; Terminate the program
    mov ah, 4ch
    int 21h

end start
