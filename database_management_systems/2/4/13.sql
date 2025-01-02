/**
  Для каждого студента напишите запрос, выводящий среднее значение оценок, полученных им по каждому предмету.
*/

WITH StudentScores AS (
    SELECT
        "STUDENT_ID",
        "SUBJ_ID" AS subject_id,
        AVG("MARK") AS average_mark
    FROM
        "EXAM_MARKS"
    GROUP BY
        "STUDENT_ID", "SUBJ_ID"
)

SELECT
    "STUDENT"."SURNAME",
    "STUDENT"."NAME",
    StudentScores.subject_id,
    StudentScores.average_mark
FROM
    StudentScores
INNER JOIN
    "STUDENT" ON StudentScores."STUDENT_ID" = "STUDENT"."STUDENT_ID";