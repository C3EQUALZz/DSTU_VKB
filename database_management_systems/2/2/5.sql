/*
 Напишите запрос для выбора из таблицы EXAM_MARKS записей, для которых отсутствуют значения оценок (поле MARK).
*/

SELECT *
FROM "EXAM_MARKS"
WHERE "MARK" IS NULL