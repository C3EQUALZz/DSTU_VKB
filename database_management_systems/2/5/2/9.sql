/*
 Напишите запрос для получения списка университетов вместе с фамилиями самых молодых студентов, обучающихся в них.
 */

SELECT "UNIV_NAME", MAX("BIRTHDAY")
FROM "UNIVERSITY"
         JOIN "STUDENT"
              ON "UNIVERSITY"."UNIV_ID" = "STUDENT"."UNIV_ID"
GROUP BY "UNIV_NAME"