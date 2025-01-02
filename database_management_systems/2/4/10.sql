/**
  Напишите запрос для определения количества предметов, изучаемых на каждом курсе.
 */

SELECT
    "KURS" AS number_of_course,
    COUNT(DISTINCT "SUBJ_ID") AS count_of_subjects
FROM "EXAM_MARKS" INNER JOIN "STUDENT" ON "EXAM_MARKS"."STUDENT_ID" = "STUDENT"."STUDENT_ID"
GROUP BY "KURS";