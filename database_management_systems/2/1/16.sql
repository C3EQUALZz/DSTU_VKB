/*
 Напишите запрос для получения списка студентов моложе 20 лет.
*/

SELECT *
FROM "STUDENT"
WHERE (extract(year from current_date) - extract (year from("BIRTHDAY"))) > 30