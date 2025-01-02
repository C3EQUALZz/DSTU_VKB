/**
  Напишите запрос, выводящий количество студентов, проживающих в каждом городе.
  Список отсортировать в порядке убывания количества студентов количества студентов.
*/

SELECT
    "CITY",
    COUNT(DISTINCT "STUDENT_ID") AS student_count
FROM
    "STUDENT"
WHERE "CITY" IS NOT NULL
GROUP BY
    "CITY"
ORDER BY
    student_count DESC;