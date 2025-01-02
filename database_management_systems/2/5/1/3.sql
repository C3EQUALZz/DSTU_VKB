/*
 Напишите запрос, выводящий список, студентов, обучающихся в Воронеже, с последующей сортировкой
 по идентификаторам университетов и курсам.
*/

SELECT
    "STUDENT"."NAME",
    "STUDENT"."SURNAME",
    "STUDENT"."UNIV_ID"
FROM "STUDENT"
WHERE LOWER("STUDENT"."CITY") = 'воронеж'
ORDER BY "STUDENT"."UNIV_ID", "STUDENT"."KURS";