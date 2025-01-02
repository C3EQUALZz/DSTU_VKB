/**
  Для каждого дня сдачи экзаменов напишите запрос,
  выводящий общее количество экзаменов, сдававшихся каждым студентом.
*/

WITH NumberOfSubjectsPassedByStudents AS (SELECT "STUDENT"."STUDENT_ID" AS student_id,
                                                 COUNT("SUBJ_ID")       AS count_of_subjects,
                                                 "EXAM_DATE"            AS "date_of_exam"
                                          FROM "EXAM_MARKS"
                                                   INNER JOIN "STUDENT" ON "STUDENT"."STUDENT_ID" = "EXAM_MARKS"."STUDENT_ID"
                                          GROUP BY "EXAM_DATE", "STUDENT"."STUDENT_ID")

SELECT "STUDENT"."SURNAME",
       "STUDENT"."NAME",
       NumberOfSubjectsPassedByStudents.count_of_subjects,
       NumberOfSubjectsPassedByStudents.date_of_exam
FROM "STUDENT"
         INNER JOIN NumberOfSubjectsPassedByStudents
                    ON "STUDENT"."STUDENT_ID" = NumberOfSubjectsPassedByStudents.student_id