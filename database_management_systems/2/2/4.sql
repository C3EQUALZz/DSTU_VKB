/*
 Напишите запрос, выбирающий сведения о студентах, у которых имена начинаются на букву 'И' или 'С'.
*/

SELECT *
FROM "STUDENT"
WHERE "NAME" LIKE 'И%' OR "NAME" LIKE 'С%'