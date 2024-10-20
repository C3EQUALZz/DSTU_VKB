@echo off
setlocal

set "max="
set "min="

:input_loop
set /p "number=Введите целое число (или '-' для завершения ввода): "

rem Проверяем, является ли введенное значение знаком '-'
if "%number%"=="-" (
    goto end_input
)

rem Проверяем, является ли введенное значение числом
for /f "delims=-0123456789" %%a in ("%number%") do (
    echo Вводите только целые числа.
    goto input_loop
)

rem Устанавливаем max и min
if not defined max (
    set "max=%number%"
    set "min=%number%"
) else (
    if %number% gtr %max% set "max=%number%"
    if %number% lss %min% set "min=%number%"
)

goto input_loop

:end_input
if defined max (
    echo Наибольшее число: %max%
    echo Наименьшее число: %min%
) else (
    echo Не введено ни одного числа.
)

endlocal
