/*
 Напишите запрос для сортировки списка университетов по значениям максимальной стипендии, выплачиваемой студентам.
 */

SELECT "UNIV_NAME", MAX("STIPEND")
FROM "UNIVERSITY" JOIN "STUDENT"
ON "UNIVERSITY"."UNIV_ID" = "STUDENT"."UNIV_ID"
GROUP BY "UNIV_NAME"