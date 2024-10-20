@echo off
setlocal

rem Проверяем, что передан параметр с каталогом
if "%~1"=="" (
    echo Укажите каталог.
    exit /b
)

rem Параметр с каталогом
set "directory=%~1"

rem Проверяем, существует ли указанный каталог
if not exist "%directory%" (
    echo Указанный каталог не существует.
    exit /b
)

rem Подсчитываем количество подкаталогов
set count=0
for /d %%D in ("%directory%\*") do (
    set /a count+=1
    call :count_subdirs "%%D"
)

echo %count%
exit /b

:count_subdirs
for /d %%D in (%1\*) do (
    set /a count+=1
    call :count_subdirs "%%D"
)
exit /b
