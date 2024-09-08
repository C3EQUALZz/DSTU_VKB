@echo off
setlocal

rem Проверяем, что переданы два параметра
if "%~1"=="" (
    echo Укажите первый каталог.
    exit /b
)
if "%~2"=="" (
    echo Укажите второй каталог.
    exit /b
)

rem Параметры
set "dir1=%~1"
set "dir2=%~2"

rem Проверяем, существуют ли указанные каталоги
if not exist "%dir1%" (
    echo Указанный первый каталог не существует.
    exit /b
)
if not exist "%dir2%" (
    echo Указанный второй каталог не существует.
    exit /b
)

rem Создаем временный файл для хранения имен файлов из первого каталога
set "tempfile=%temp%\files1.txt"
dir /b "%dir1%\*" > "%tempfile%"

rem Используем один оператор FOR для проверки наличия файлов во втором каталоге
echo Файлы, присутствующие в обоих каталогах:
for /f "delims=" %%f in ('dir /b "%dir2%\*"') do (
    findstr /x /i "%%f" "%tempfile%" >nul && echo %%f
)

rem Удаляем временный файл
del "%tempfile%"

endlocal
