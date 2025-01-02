/*
 Напишите запрос, выполняющий вывод из таблицы EXAM_MARKS записей, для которых в поле MARK проставлены значения оценок.
*/

SELECT *
FROM "EXAM_MARKS"
WHERE "MARK" IS NOT NULL