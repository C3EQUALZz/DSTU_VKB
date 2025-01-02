/*
 Напишите запрос, выводящий список студентов, получающих максимальную стипендию,
 отсортировав его в алфавитном порядке по фамилиям.
*/

WITH ScholarShip AS (
    SELECT MAX("STUDENT"."STIPEND") AS max_scholarship
    FROM "STUDENT"
)

SELECT
    "STUDENT"."NAME",
    "STUDENT"."SURNAME"
FROM "STUDENT"
WHERE "STUDENT"."STIPEND" = (SELECT max_scholarship FROM ScholarShip);