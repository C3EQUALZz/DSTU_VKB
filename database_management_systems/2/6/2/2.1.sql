/*
 Пусть существует таблица с именем STUDENT1, определения столбцов которой полностью совпадают с
 определениями столбцов таблицы STUDENT.
 Вставьте в эту таблицу сведения о студентах, успешно сдавших экзамены более чем по пяти предметам обучения
 */

CREATE TABLE STUDENT1 AS (SELECT *
                          FROM "STUDENT");

WITH StudentsWhoPassedExamsInCountOfSubjects AS (
    SELECT "STUDENT"."STUDENT_ID"
    FROM "STUDENT" INNER JOIN "EXAM_MARKS" ON "STUDENT"."STUDENT_ID" = "EXAM_MARKS"."STUDENT_ID"
    WHERE "EXAM_MARKS"."MARK" >= 3
    GROUP BY "STUDENT"."STUDENT_ID"
    HAVING COUNT("STUDENT"."STUDENT_ID") > 5
)

INSERT INTO STUDENT1 ("STUDENT_ID", "SURNAME", "NAME", "STIPEND", "KURS", "CITY", "BIRTHDAY", "UNIV_ID")
SELECT "STUDENT".*
FROM "STUDENT" INNER JOIN StudentsWhoPassedExamsInCountOfSubjects ON "STUDENT"."STUDENT_ID" = StudentsWhoPassedExamsInCountOfSubjects."STUDENT_ID"

