/*
 Вывести преподавателей и дисциплины, по которым в таблице оценок для обучающихся студентов в текущем семестре есть
 незаполненные (пустые) оценки.
 */

-- Тут очень странно поставлено условие. Тут нет такого случая, когда Mark может иметь NULL.

SELECT
    "Prepod"."PrepodFamIO" AS teacher_name,
    "Plany"."PDiscipline" AS discipline_code
FROM
    "Mark"
FULL JOIN "StudPlany" ON "Mark"."TStudPlan" = "StudPlany"."IDStudPlan"
FULL JOIN "Plany" ON "StudPlany"."GroopPlan" = "Plany"."IDPlany"
FULL JOIN "Prepod" ON "Plany"."IDPlany" = "Prepod"."PlanyID"
FULL JOIN "StudentsT" ON "StudPlany"."Student" = "StudentsT"."IDStudent"
WHERE
    "Mark"."Mark" IS NULL AND "StudentsT"."Semestr" = "Plany"."PSemestr";

