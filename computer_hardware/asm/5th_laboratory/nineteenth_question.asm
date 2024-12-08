.model small
.stack 100h

.data
    input_string db 50 dup('$')      ; Buffer for input string
    output_msg db 'Number of commas: $'
    comma_count dw 0                  ; Counter for commas (2 bytes)
    newline db 0dh, 0ah, '$'

.code
start:
    mov ax, @data
    mov ds, ax

    ; Prompt user to enter a string
    lea dx, input_string              ; Address of the buffer for input string
    mov ah, 0Ah                       ; Function to read string input
    int 21h

    ; Print a new line
    lea dx, newline
    mov ah, 09h
    int 21h

    ; Initialize comma counter
    xor ax, ax                        ; Clear AX register (counter)
    lea si, input_string + 2          ; Point to the first character of the string
    mov bl, input_string[1]           ; Get the length of the input string

count_commas:
    cmp bl, 0                          ; Check if we reached the end of the string
    je print_result                    ; If end of string, jump to result output
    cmp byte ptr [si], ','             ; Compare with comma
    jne next_char                      ; If not a comma, jump to next character
    inc word ptr [comma_count]        ; Increment the comma count
next_char:
    inc si                             ; Move to the next character
    dec bl                             ; Decrease length counter
    jmp count_commas                  ; Repeat the counting loop

print_result:
    ; Output the result
    lea dx, output_msg                 ; Address of the output message
    mov ah, 09h                        ; Function to output string
    int 21h

    ; Print the number of commas
    mov ax, comma_count                ; Load comma count into AX
    call PrintNumber                   ; Call subroutine to print the number

    ; Terminate the program
    mov ah, 4Ch
    int 21h

; Subroutine to print the number in AX
PrintNumber:
    ; Convert number in AX to string
    xor cx, cx                         ; Clear CX (digit count)
    mov bx, 10                         ; Divisor for decimal conversion
next_digit:
    xor dx, dx                         ; Clear DX before division
    div bx                              ; AX / 10, remainder in DX
    push dx                             ; Push remainder (digit)
    inc cx                              ; Increment digit count
    test ax, ax                        ; Check if number is now 0
    jnz next_digit                     ; If not 0, continue

print_digits:
    pop dx                              ; Pop the last digit
    add dl, '0'                        ; Convert to ASCII
    mov ah, 02h                        ; Function to output character
    int 21h                            ; Output the character
    loop print_digits                   ; Repeat for all digits

    ret

end start
