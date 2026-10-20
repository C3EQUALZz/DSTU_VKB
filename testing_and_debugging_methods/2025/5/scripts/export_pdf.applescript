-- Экспорт только указанного DOCX; другие документы Word не затрагиваются.
on run argv
    set sourcePath to item 1 of argv
    set outputPath to item 2 of argv
    with timeout of 300 seconds
        tell application "Microsoft Word"
            open file name sourcePath
            set labDocument to active document
            save as labDocument file name outputPath file format format PDF
            close labDocument saving no
        end tell
    end timeout
end run
