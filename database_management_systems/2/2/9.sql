/*
 Напишите запрос для получения списка студентов, фамилии которых начинаются на 'Ков' или на 'Куз'.
*/

SELECT *
FROM "STUDENT"
WHERE "SURNAME" LIKE 'Ков%' OR "SURNAME" LIKE 'Куз%'