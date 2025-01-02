/*
 Напишите запрос, который позволяет подсчитать в таблице EXAM_MARKS
 количество различных предметов обучения (использовать оператор DISTINCT.
*/

SELECT COUNT(DISTINCT "SUBJ_ID")
FROM "EXAM_MARKS";