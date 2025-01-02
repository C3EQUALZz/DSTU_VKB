/*
 Напишите запрос, выводящий список студентов, получающих стипендию, превышающую среднее значение стипендии.
*/

WITH ScholarShip AS (
    SELECT AVG("STUDENT"."STIPEND") AS avg_scholarship
    FROM "STUDENT"
)

SELECT
    "STUDENT"."SURNAME",
    "STUDENT"."NAME",
    "STUDENT"."KURS"
FROM "STUDENT"
WHERE "STUDENT"."STIPEND" >= (SELECT avg_scholarship FROM ScholarShip);