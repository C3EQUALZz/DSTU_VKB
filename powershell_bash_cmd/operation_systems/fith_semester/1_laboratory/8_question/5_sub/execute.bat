@echo off
setlocal
set fact=1
set /p num="Введите число: "

call :fact %num%
echo %errorlevel%
goto :eof

:fact
set /a fact*=num , num-=1
if %num% gtr 0 call :fact
exit /b %fact%
