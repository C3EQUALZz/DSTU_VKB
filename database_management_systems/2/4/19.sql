/**
  Для каждого дня сдачи экзаменов напишите запрос, выводящий среднее значение всех экзаменационных оценок.
 */

SELECT AVG("MARK"), "EXAM_DATE"
FROM "EXAM_MARKS"
GROUP BY "EXAM_DATE"