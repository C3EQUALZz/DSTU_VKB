.MODEL TINY
.STACK 100h
.DATA
    charPercent db '%', '$'   ; String to output the '%'
    rowCounter db 0           ; Row counter
    colCounter db 0           ; Column counter
.CODE

Start:
    ; Main program loop
MainLoop:
    ; Wait for a key press
    mov ah, 01h               ; Function 01h to read a character
    int 21h                   ; Call DOS to read the character
    cmp al, 1Bh               ; Check if Esc key is pressed
    je EndProgram             ; If Esc, terminate the program

    ; Set cursor to coordinates (colCounter, rowCounter)
    mov ah, 02h               ; Function to set the cursor
    mov bh, 0                 ; Page (usually 0 for a single screen)
    mov dh, rowCounter         ; Vertical position (Y)
    mov dl, colCounter         ; Horizontal position (X)
    int 10h                   ; Call BIOS to set the cursor

    ; Output the '%'
    mov ah, 09h               ; Function to output a string
    lea dx, charPercent        ; Load address of the string
    int 21h                   ; Call DOS to output the string

    ; Update coordinates
    inc colCounter             ; Increment the column
    cmp colCounter, 80        ; Check for boundary overflow
    jb ContinueCol
    mov colCounter, 0         ; Reset column
ContinueCol:
    inc rowCounter             ; Increment the row
    cmp rowCounter, 24        ; Check for boundary overflow
    jb MainLoop               ; Continue if we haven't reached 24
    mov rowCounter, 0         ; Reset row

    jmp MainLoop              ; Return to main loop

EndProgram:
    ; Terminate the program
    mov ah, 4Ch               ; Function to terminate the program
    int 21h                   ; Call DOS to exit

end Start
