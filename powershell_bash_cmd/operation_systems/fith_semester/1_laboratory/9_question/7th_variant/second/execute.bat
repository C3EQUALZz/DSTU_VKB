@echo off
setlocal enabledelayedexpansion

:: Проверяем, был ли передан каталог в качестве первого параметра
if "%~1"=="" (
    echo Ошибка: Каталог не указан.
    goto end
)

:: Проверяем, существует ли указанный каталог
if not exist "%~1" (
    echo Ошибка: Указанный каталог не существует.
    goto end
)

:: Проверяем наличие файла Numbers.txt в указанном каталоге
set filePath=%~1\Numbers.txt
if not exist "%filePath%" (
    echo Ошибка: Файл Numbers.txt не найден в каталоге %~1.
    goto end
)

:: Если файл существует, создаем новый файл с суммами
set outputFile=%~1\Result.txt
echo Обрабатываем файл %filePath%...

:: Чтение и обработка файла
(for /f "tokens=1,2" %%a in ('type "%filePath%"') do (
    set col1=%%a
    set col2=%%b

    :: Удаление пробелов из чисел, если они есть
    set col1=!col1!
    set col2=!col2!

    :: Вычисление суммы
    set /a sum=!col1!+!col2!

    :: Запись в новый файл
    echo !col1!   !col2!   !sum! >> "%outputFile%"
)) || (
    echo Ошибка при обработке файла.
    goto end
)

echo Файл обработан успешно. Результат сохранен в %outputFile%.

:end
