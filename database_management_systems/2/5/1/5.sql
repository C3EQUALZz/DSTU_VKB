/*
 Напишите запрос, выполняющий вывод имен и фамилий студентов, место проживания
 которых не совпадает с городом, в котором находится их университет.
 */

SELECT
    "STUDENT"."NAME" AS name,
    "STUDENT"."SURNAME" AS surname
FROM "STUDENT" INNER JOIN "UNIVERSITY" ON "STUDENT"."UNIV_ID" = "UNIVERSITY"."UNIV_ID"
WHERE "UNIVERSITY"."CITY" != "STUDENT"."CITY"