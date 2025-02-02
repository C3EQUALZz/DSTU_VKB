/*
 Найти всех отчисленных студентов, у которых есть хотя бы одна задолженность.
 */

SELECT
    "StudentsT"."IDStudent" AS student_id,
    "Persons"."Фам" || ' ' || "Persons"."Имя" || ' ' || "Persons"."Отч" AS student_name,
    "StudPlany"."ResultMark" AS result_mark
FROM
    "StudentsT"
JOIN "PersonT" ON "StudentsT"."IDPerson" = "PersonT"."IDPerson"
JOIN "Persons" ON "PersonT"."IDPerson" = "Persons"."IDPersons"
JOIN "StudPlany" ON "StudentsT"."IDStudent" = "StudPlany"."Student"
WHERE
    -- "StudentsT"."LearnStatus" = 'D'  -- статус отчисленных студентов (предположительно "D")
    -- AND ("StudPlany"."ResultMark" IS NULL OR "StudPlany"."ResultMark" < 50);
    "StudPlany"."ResultMark" IS NULL