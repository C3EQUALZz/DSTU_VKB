/**
  Напишите запрос, выдающий средний балл для каждого экзамена.
 */

SELECT AVG("MARK")
FROM "EXAM_MARKS"
GROUP BY "SUBJ_ID"