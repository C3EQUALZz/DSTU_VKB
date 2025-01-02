/**
  Для каждого дня сдачи экзаменов напишите запрос, выводящий максимальные оценки, полученные по каждому предмету.
*/

SELECT
    "SUBJ_NAME" AS subject_name,
    MAX("MARK") AS maximal_mark,
    "EXAM_DATE"
FROM "EXAM_MARKS" INNER JOIN "SUBJECT" ON "EXAM_MARKS"."SUBJ_ID" = "SUBJECT"."SUBJ_ID"
GROUP BY "EXAM_DATE", "SUBJ_NAME";