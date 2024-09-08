@echo off
setlocal

rem Проверяем, что переданы два параметра
if "%~1"=="" (
    echo Вы не указали каталог.
    exit /b
)
if "%~2"=="" (
    echo Вы не указали расширение файлов.
    exit /b
)

rem Параметры
set "directory=%~1"
set "extension=%~2"

rem Проверяем, существует ли указанный каталог
if not exist "%directory%" (
    echo Указанный каталог не существует.
    exit /b
)

rem Выводим имена файлов с указанным расширением
echo Файлы с расширением %extension% в каталоге %directory%:
for %%f in ("%directory%\*.%extension%") do (
    echo %%~nxf
)

endlocal
