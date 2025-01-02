/**
  Напишите запрос, определяющий количество сдававших студентов для каждого экзамена.
 */

SELECT COUNT(DISTINCT "STUDENT_ID")
FROM "EXAM_MARKS"
GROUP BY "SUBJ_ID"