on run argv
    set basePath to item 1 of argv
    set calculationPdf to basePath & "/Расчетная_часть_99.pdf"
    set reportPdf to basePath & "/отчет_99_расчеты_обновлены.pdf"
    if (count of argv) > 1 then
        if item 2 of argv is "status" then
            with timeout of 15 seconds
                tell application "Microsoft Word"
                    set display alerts to alerts none
                    return name of documents
                end tell
            end timeout
        end if
        if item 2 of argv is "preview2" then
            set calculationPdf to basePath & "/report_assets/calculations_preview_v2.pdf"
            set reportPdf to basePath & "/report_assets/report_preview_v2.pdf"
        end if
    end if
    with timeout of 30 seconds
        tell application "Microsoft Word"
            set display alerts to alerts none
            open POSIX file (basePath & "/Расчетная_часть_99.docx")
            set calculationDocument to active document
            save as calculationDocument file name calculationPdf file format format PDF
            close calculationDocument saving no
            open POSIX file (basePath & "/отчет_99_расчеты_обновлены.docx")
            set reportDocument to active document
            save as reportDocument file name reportPdf file format format PDF
            close reportDocument saving no
        end tell
    end timeout
    return "PDF экспортированы"
end run
