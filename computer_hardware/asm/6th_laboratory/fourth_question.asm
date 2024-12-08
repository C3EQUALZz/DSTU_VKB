; Разработать две подпрограммы, одна из которых сравнивает две строки по лексикографическому порядку, а другая обменивает значения двух строк.
; Разработать программу, которая вводит с клавиатуры несколько строк (конец ввода пустая строка) и сортирует их в лексикографическом порядке.

DATA_S SEGMENT
    MSG1 DB 0DH, 0AH, "ENTER FIRST STROKE : $", 0DH, 0AH
    MSG2 DB 0DH, 0AH, "ENTER SECOND STROKE : $", 0DH, 0AH
    MSG_FIRST DB 0DH, 0AH, "FIRST STROKE CONTAINS SECOND STROKE$", 0DH, 0AH
    MSG_SECOND DB 0DH, 0AH, "SECOND STROKE CONTAINS FIRST STROKE$", 0DH, 0AH
    MSG_COUNT DB 0DH, 0AH, "HOW MANY TIMES: $", 0DH, 0AH
    MSG_NO DB 0DH, 0AH, "NO ENTRANCES$"
    STR1HEAD DB 80
    STR1LEN DB ?
    STR1 DB 80 DUP(?)
    STR2HEAD DB 80
    STR2LEN DB ?
    STR2 DB 80 DUP(?)
    COUNT DB 0
    ENTRYIDX DB ?
    STARTIDX DW ?
    LOOPCOUNTER DB ?
    SWAPPED DB 0
DATA_S ENDS
CODE_S SEGMENT
    ASSUME CS:CODE_S, DS:DATA_S
    WRITENUM PROC
        PUSHA
        MOV AL, COUNT
        MOV CX, 10
        MOV BX, 0
        ADDITION_LOOP:
            XOR DX, DX
            DIV CX
            ADD DL, '0'
            PUSH DX
            INC BX
            CMP AL, 0
            JNE ADDITION_LOOP
        PRINT_LOOP:
            POP DX
            MOV AH, 02H
            INT 21H
            DEC BX
            CMP BX, 0
            JNE PRINT_LOOP
        POPA
        RET
    WRITENUM ENDP

    STR_OUTPUT PROC
        PUSHA
        MOV AH, 09H
        INT 21H
        POPA
        RET
    STR_OUTPUT ENDP

    STR_INPUT PROC
        PUSHA
        MOV AH, 0AH
        INT 21H
        POPA
        RET
    STR_INPUT ENDP

    COUNT_ENTRANCES PROC
        LEA SI, [STR1]
        LEA DI, [STR2]
        MOV AL, STR1LEN   ; LENGTH STR1
        MOV AH, 0
        MOV BL, STR2LEN   ; LENGTH STR2
        MOV BH, 0
        MOV STARTIDX, 0   ; INDEX OF NEXT STROKE START
        CMP AX, BX
        JNB CMP_LOOP
        SWAP:   ; SWAPPING STR1 AND STR2
            MOV SWAPPED, 1H
            XCHG SI, DI
            XCHG AX, BX
        CMP_LOOP:
            ADD SI, STARTIDX ; ADDR OF STR = PREV ADDR + START
            CALL FIND_SUBSTR
        PROCESSING:
            MOV DH, 0
            MOV DL, ENTRYIDX
            DEC DX      ; ENTRYIDX
            CMP DX, -1  ; NO MORE ENTRANCES
        JE EXIT
            INC COUNT
            MOV STARTIDX, BX
            ADD STARTIDX, DX ; STARTIDX = ENTRYIDX + SUBSTR LENGTH
            PUSH CX
            MOV CX, STARTIDX
            ADD CX, BX      ; CX = STARTIDX + SUBLEN
            CMP AX, CX ; STRLEN >= STARTIDX + SUBLEN?
            POP CX
        JB EXIT
            JMP CMP_LOOP
        EXIT:
            RET
    COUNT_ENTRANCES ENDP
    FIND_SUBSTR PROC
        PUSHA
        MOV CX, STARTIDX
        SBB AL, CL
        MOV CL, AL  ; CL - LENGTH STROKE
        MOV CH, BL  ; CH - LENGTH SUBSTROKE
        CMP CL, CH        ; LEN(STR) >= LEN(SUB)
        MOV LOOPCOUNTER, CL
        JB RETURN
        MOV DH, 0           ; INDEX OF CURRENT CHAR
        MOV ENTRYIDX, 0     ; INDEX OF FIRST ENTRANCE
        MOV BL, 0           ; NUMBER OF CHARACTERS FOUND IN A ROW
        NEXT_VAL:
            INC DH          ; INCREASE CHAR INDEX
            MOV AL, [SI]
            MOV AH, [DI + BX]
            INC SI          ; INCREASE CHAR ADDRESS
            CMP AL, AH      ; COMPARING CURRENT STRING CHAR
                            ; WITH INDEXED SUBSTRING CHAR
            JE EQUAL
        NOT_EQUAL:
            MOV BL, 0       ; RESET COUNTER
            MOV ENTRYIDX, 0       ; RESET ENTRANCE INDEX
            MOV AH, [DI]
            CMP AL, AH
            JE EQUAL
            CMP LOOPCOUNTER, 0
            JE RETURN      ; WASNT FOUND
            DEC LOOPCOUNTER
            JMP NEXT_VAL
        EQUAL:
            CMP ENTRYIDX, 0
            JNE SKIP_INDEX  ; IF CHAR IS NOT ENTRANCE
            MOV ENTRYIDX, DH
            SKIP_INDEX:
            INC BL          ; INCREASE SUBSTRING COUNTER
            CMP BL, CH      ; SUBSTR COUNTER == LENGTH OF SUBSTRING?
            JZ RETURN
            CMP LOOPCOUNTER, 0
            JE RETURN
            DEC LOOPCOUNTER
            JMP NEXT_VAL
        RETURN:
            POPA
            RET
    FIND_SUBSTR ENDP
    START:
        MOV AX, DATA_S
        MOV DS, AX
        XOR CX, CX
        ; STR1
        LEA DX, MSG1
        CALL STR_OUTPUT
        LEA DX, STR1HEAD
        CALL STR_INPUT
        ; STR2
        LEA DX, MSG2
        CALL STR_OUTPUT
        LEA DX, STR2HEAD
        CALL STR_INPUT
        ; LOGIC
        CALL COUNT_ENTRANCES
        CMP COUNT, 0
        JE NO
        CMP SWAPPED, 1
        JE SECOND
        FIRST:
        LEA DX, MSG_FIRST
        JMP OUTPUT
        SECOND:
        LEA DX, MSG_SECOND
        JMP OUTPUT
        NO:
        LEA DX, MSG_NO
        CALL STR_OUTPUT
        JMP QUIT
        OUTPUT:
        CALL STR_OUTPUT
        COUNT_OUTPUT:
        LEA DX, MSG_COUNT
        CALL STR_OUTPUT
        CALL WRITENUM
    QUIT:
        MOV AX, 4C00H
        INT 21H
CODE_S ENDS
END START
