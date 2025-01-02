/*
 Напишите запрос для получения списка студентов старше 25 лет, обучающихся на 1-м курсе.
 */

SELECT *
FROM "STUDENT"
WHERE "KURS" = 1 AND EXTRACT(YEAR FROM AGE(NOW(), "BIRTHDAY")) > 25;