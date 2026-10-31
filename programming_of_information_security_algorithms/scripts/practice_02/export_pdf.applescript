-- Экспорт только указанного отчёта; остальные документы Word не затрагиваются.
on run argv
    if (count of argv) is not 2 then error "Ожидаются абсолютные пути DOCX и PDF"
    set sourceFile to POSIX file (item 1 of argv) as alias
    set destinationFile to item 2 of argv
    with timeout of 120 seconds
        tell application "Microsoft Word"
            activate
            open sourceFile read only true add to recent files false
            set reportDocument to active document
            -- Приложение сохраняет в собственную разрешённую временную папку.
            set temporaryFolder to POSIX path of (path to temporary items)
            set temporaryPdf to temporaryFolder & "practice_02_preview.pdf"
            save as reportDocument file name temporaryPdf file format format PDF
            close reportDocument saving no
        end tell
    end timeout
    do shell script "/bin/cp " & quoted form of temporaryPdf & " " & quoted form of destinationFile
    return destinationFile
end run
