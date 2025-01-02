/**
  Напишите запрос, выдающий средний балл для каждого студента.
*/

SELECT AVG("MARK")
FROM "EXAM_MARKS"
GROUP BY "STUDENT_ID"