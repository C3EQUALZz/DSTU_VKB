/*
 Напишите запрос, увеличивающий размер стипендии на 20% всем студентам,
 у которых общая сумма баллов превышает значение 50.
 */

UPDATE "STUDENT"
SET "STIPEND" = 1.2 * "STIPEND"
WHERE "STUDENT"."STUDENT_ID" IN (SELECT "STUDENT"."STUDENT_ID"
                                 FROM "EXAM_MARKS"
                                          INNER JOIN "STUDENT" ON "EXAM_MARKS"."STUDENT_ID" = "STUDENT"."STUDENT_ID"
                                 GROUP BY "STUDENT"."STUDENT_ID"
                                 HAVING SUM("MARK") > 50)