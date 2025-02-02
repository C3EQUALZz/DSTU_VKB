/*
 Выведите пронумерованный список ста первых студентов, у которых средний итоговый балл (StudPlany.ResultMark)
 за весь период обучения наибольший (без учета пустых значений).
 Список отсортировать по алфавиту. Вывести: Фамилию И.О., зачетная книжка, средний итоговый балл, позиция в списке 100.
 */

WITH AverageMarksOfStudents AS (
    SELECT
        "StudentsT"."IDStudent"  AS student_id,
        AVG(CAST("StudPlany"."ResultMark" AS NUMERIC)) AS average_mark_of_student
    FROM "StudentsT" INNER JOIN "StudPlany" ON "StudentsT"."IDStudent" = "StudPlany"."Student"
    GROUP BY "StudentsT"."IDStudent"
),
    RankedStudents AS (
    SELECT
        "Persons"."Фам",
        "Persons"."Имя",
        "Persons"."Отч",
        "PersonT"."Номер зачетки",
        ROW_NUMBER() OVER (ORDER BY "Persons"."Фам", "Persons"."Имя", "Persons"."Отч") AS position
    FROM "Persons"
    INNER JOIN AverageMarksOfStudents ON "Persons"."IDPersons" = AverageMarksOfStudents.student_id
    INNER JOIN "PersonT" ON "Persons"."IDPersons" = "PersonT"."IDPerson"
)

SELECT
    RankedStudents."Фам",
    RankedStudents."Имя",
    RankedStudents."Отч",
    RankedStudents."Номер зачетки",
    position
FROM RankedStudents
WHERE position <= 100
ORDER BY RankedStudents."Фам", RankedStudents."Имя", RankedStudents."Отч";
