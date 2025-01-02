/*
 Напишите запрос, выполняющий вывод количества студентов, имеющих только отличные оценки.
*/

SELECT COUNT("STUDENT_ID")
FROM "EXAM_MARKS"
WHERE "MARK" = 5
