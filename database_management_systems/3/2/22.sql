/*
 Для обучающихся студентов посчитать количество дисциплин (без повторов), которые будут им преподаваться в следующем
 семестре (текущий семестр установлен у объекта «Студент»).
 */

SELECT
    "StudentsT"."IDStudent" AS student_id,
    COUNT(DISTINCT "Plany"."PDiscipline") AS count_of_subjects
FROM "StudentsT"
    INNER JOIN "StudPlany" ON "StudentsT"."IDStudent" = "StudPlany"."Student"
    INNER JOIN "Plany" ON "StudPlany"."GroopPlan" = "Plany"."IDPlany"
WHERE "StudentsT"."Semestr" + 1 = "Plany"."PSemestr"
GROUP BY "StudentsT"."IDStudent";