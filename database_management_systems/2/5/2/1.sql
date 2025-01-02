/*
 Напишите запрос для получения списка университетов с указанием количества студентов, обучающихся на каждом курсе.
 */

SELECT "UNIV_NAME", "KURS", COUNT("STUDENT_ID")
FROM "UNIVERSITY"
         JOIN "STUDENT"
              ON "UNIVERSITY"."UNIV_ID" = "STUDENT"."UNIV_ID"
GROUP BY "UNIV_NAME", "KURS"