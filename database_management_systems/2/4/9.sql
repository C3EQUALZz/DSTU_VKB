/**
  Напишите запрос, определяющий количество сдававших студентов для каждого экзамена.
 */

SELECT "SUBJ_ID", COUNT(DISTINCT "STUDENT_ID")
FROM "EXAM_MARKS"
GROUP BY "SUBJ_ID"